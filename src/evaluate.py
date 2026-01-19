"""Main evaluation script for multilingual LLM experiments."""
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from tqdm import tqdm
import numpy as np

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    MODELS, XNLI_LANGUAGES, RESULTS_DIR, SEED,
    SAMPLE_SIZE_XNLI, NLI_LABELS, LANGUAGE_NAMES
)
from data_loader import load_xnli_samples
from llm_api import create_client
from prompts import (
    format_nli_prompt, format_translation_prompt,
    parse_nli_response, NLI_SYSTEM_PROMPT
)


def evaluate_nli_direct(
    client,
    samples: Dict[str, List[Dict]],
    languages: List[str],
    model_name: str
) -> Dict[str, Dict]:
    """
    Evaluate NLI task directly in each language.

    Returns dict mapping language -> {accuracy, predictions, labels}
    """
    results = {}

    for lang in languages:
        if lang not in samples or not samples[lang]:
            print(f"  Skipping {lang}: no samples")
            continue

        lang_samples = samples[lang]
        predictions = []
        labels = []

        print(f"  Evaluating {lang} ({LANGUAGE_NAMES.get(lang, lang)})...")

        for sample in tqdm(lang_samples, desc=f"    {lang}", leave=False):
            prompt = format_nli_prompt(
                sample["premise"],
                sample["hypothesis"],
                language=lang
            )

            try:
                response = client.complete(
                    prompt,
                    system_prompt=NLI_SYSTEM_PROMPT["multilingual"]
                )
                pred = parse_nli_response(response)
            except Exception as e:
                print(f"      Error: {e}")
                pred = "neutral"  # Default on error

            predictions.append(pred)
            labels.append(sample["label_name"])

        # Calculate accuracy
        correct = sum(1 for p, l in zip(predictions, labels) if p == l)
        accuracy = correct / len(labels) if labels else 0

        results[lang] = {
            "accuracy": accuracy,
            "n_samples": len(labels),
            "predictions": predictions,
            "labels": labels,
            "correct": correct
        }

        print(f"    {lang}: {accuracy:.2%} ({correct}/{len(labels)})")

    return results


def evaluate_nli_translate_test(
    client,
    samples: Dict[str, List[Dict]],
    english_samples: Dict[str, List[Dict]],
    languages: List[str],
    model_name: str
) -> Dict[str, Dict]:
    """
    Evaluate NLI using translate-to-English approach.

    For each non-English sample, translate to English first, then evaluate.
    Uses the parallel English samples as ground truth translations.
    """
    results = {}

    # Get English sample indices for lookup
    en_by_idx = {s["index"]: s for s in english_samples.get("en", [])}

    for lang in languages:
        if lang == "en" or lang not in samples:
            continue

        lang_samples = samples[lang]
        predictions = []
        labels = []

        print(f"  Translate-test {lang}...")

        for sample in tqdm(lang_samples, desc=f"    {lang}", leave=False):
            # Use the parallel English translation (already available in dataset)
            idx = sample["index"]
            if idx in en_by_idx:
                en_sample = en_by_idx[idx]
                prompt = format_nli_prompt(
                    en_sample["premise"],
                    en_sample["hypothesis"],
                    language="en"
                )

                try:
                    response = client.complete(
                        prompt,
                        system_prompt=NLI_SYSTEM_PROMPT["en"]
                    )
                    pred = parse_nli_response(response)
                except Exception as e:
                    print(f"      Error: {e}")
                    pred = "neutral"

                predictions.append(pred)
                labels.append(sample["label_name"])

        # Calculate accuracy
        correct = sum(1 for p, l in zip(predictions, labels) if p == l)
        accuracy = correct / len(labels) if labels else 0

        results[lang] = {
            "accuracy": accuracy,
            "n_samples": len(labels),
            "predictions": predictions,
            "labels": labels,
            "correct": correct,
            "method": "translate_test"
        }

        print(f"    {lang}: {accuracy:.2%} ({correct}/{len(labels)})")

    return results


def run_experiment(
    model_name: str,
    languages: Optional[List[str]] = None,
    n_samples: int = SAMPLE_SIZE_XNLI
) -> Dict:
    """Run full evaluation experiment for a model."""
    if languages is None:
        languages = XNLI_LANGUAGES

    print(f"\n{'='*60}")
    print(f"Evaluating: {model_name}")
    print(f"{'='*60}")

    # Create client
    try:
        client = create_client(model_name, MODELS)
    except Exception as e:
        print(f"Error creating client: {e}")
        return {}

    # Load data
    print("\nLoading XNLI samples...")
    samples = load_xnli_samples(languages=languages, n_samples=n_samples)

    # Report sample counts
    for lang in languages:
        n = len(samples.get(lang, []))
        print(f"  {lang}: {n} samples")

    # Direct evaluation
    print("\n--- Direct Evaluation (native language prompts) ---")
    direct_results = evaluate_nli_direct(client, samples, languages, model_name)

    # Translate-test evaluation
    print("\n--- Translate-Test Evaluation ---")
    translate_results = evaluate_nli_translate_test(
        client, samples, samples, languages, model_name
    )

    # Compile results
    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "n_samples_per_lang": n_samples,
        "languages": languages,
        "direct": direct_results,
        "translate_test": translate_results
    }

    return results


def save_results(results: Dict, filename: str):
    """Save results to JSON file."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    filepath = os.path.join(RESULTS_DIR, filename)

    # Convert results to serializable format
    serializable = {}
    for key, value in results.items():
        if key in ["direct", "translate_test"]:
            serializable[key] = {}
            for lang, lang_results in value.items():
                serializable[key][lang] = {
                    k: v for k, v in lang_results.items()
                    if k != "predictions"  # Don't save all predictions
                }
                serializable[key][lang]["accuracy"] = round(lang_results["accuracy"], 4)
        else:
            serializable[key] = value

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {filepath}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate multilingual LLM performance")
    parser.add_argument(
        "--model", type=str, default=None,
        help="Model to evaluate (default: all)"
    )
    parser.add_argument(
        "--languages", type=str, nargs="+", default=None,
        help="Languages to evaluate (default: all XNLI languages)"
    )
    parser.add_argument(
        "--n-samples", type=int, default=SAMPLE_SIZE_XNLI,
        help="Number of samples per language"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output filename (default: auto-generated)"
    )

    args = parser.parse_args()

    # Determine which models to evaluate
    models_to_eval = [args.model] if args.model else list(MODELS.keys())

    all_results = {}

    for model_name in models_to_eval:
        if model_name not in MODELS:
            print(f"Unknown model: {model_name}")
            continue

        results = run_experiment(
            model_name,
            languages=args.languages,
            n_samples=args.n_samples
        )

        if results:
            all_results[model_name] = results

            # Save individual model results
            output_file = args.output or f"results_{model_name.replace('.', '_')}.json"
            save_results(results, output_file)

    # Save combined results
    if len(all_results) > 1:
        combined_file = "results_combined.json"
        with open(os.path.join(RESULTS_DIR, combined_file), "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\nCombined results saved to: {combined_file}")

    return all_results


if __name__ == "__main__":
    main()
