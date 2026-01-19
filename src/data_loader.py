"""Data loading utilities for multilingual LLM evaluation."""
import random
from datasets import load_from_disk
from typing import Dict, List, Tuple, Optional
from config import (
    DATASET_PATHS, XNLI_LANGUAGES, SAMPLE_SIZE_XNLI, SAMPLE_SIZE_SIB200,
    NLI_LABELS, SIB200_CATEGORIES, SEED
)

random.seed(SEED)


def load_xnli_samples(
    languages: Optional[List[str]] = None,
    n_samples: int = SAMPLE_SIZE_XNLI,
    split: str = "test"
) -> Dict[str, List[Dict]]:
    """
    Load XNLI samples for specified languages.

    Returns a dict mapping language code to list of samples.
    Each sample is a dict with keys: 'premise', 'hypothesis', 'label', 'label_name'
    """
    if languages is None:
        languages = XNLI_LANGUAGES

    dataset = load_from_disk(DATASET_PATHS["xnli"])
    data = dataset[split]

    # Sample indices
    n_total = len(data)
    indices = random.sample(range(n_total), min(n_samples, n_total))

    samples_by_lang = {lang: [] for lang in languages}

    for idx in indices:
        item = data[idx]
        label_idx = item["label"]
        label_name = NLI_LABELS[label_idx]

        # Get hypothesis for each language
        hypothesis_langs = item["hypothesis"]["language"]
        hypothesis_translations = item["hypothesis"]["translation"]

        for lang in languages:
            if lang in item["premise"] and lang in hypothesis_langs:
                h_idx = hypothesis_langs.index(lang)
                sample = {
                    "premise": item["premise"][lang],
                    "hypothesis": hypothesis_translations[h_idx],
                    "label": label_idx,
                    "label_name": label_name,
                    "index": idx
                }
                samples_by_lang[lang].append(sample)

    return samples_by_lang


def load_sib200_samples(
    languages: Optional[List[str]] = None,
    n_samples: int = SAMPLE_SIZE_SIB200,
    split: str = "test"
) -> Dict[str, List[Dict]]:
    """
    Load SIB-200 samples for specified languages.

    Returns a dict mapping language code to list of samples.
    Each sample is a dict with keys: 'text', 'category', 'index_id'
    """
    # Map language codes to SIB-200 codes
    lang_to_sib = {
        "en": "eng_Latn", "de": "deu_Latn", "fr": "fra_Latn", "es": "spa_Latn",
        "ar": "arb_Arab", "zh": "zho_Hans", "ja": "jpn_Jpan", "ko": "kor_Hang"
    }

    if languages is None:
        languages = list(lang_to_sib.keys())

    samples_by_lang = {}

    for lang in languages:
        sib_code = lang_to_sib.get(lang)
        if sib_code is None:
            continue

        try:
            dataset_path = f"{DATASET_PATHS['sib200']}/{sib_code}"
            dataset = load_from_disk(dataset_path)
            data = dataset[split]

            n_total = len(data)
            indices = random.sample(range(n_total), min(n_samples, n_total))

            samples = []
            for idx in indices:
                item = data[idx]
                samples.append({
                    "text": item["text"],
                    "category": item["category"],
                    "index_id": item["index_id"],
                    "index": idx
                })

            samples_by_lang[lang] = samples
        except Exception as e:
            print(f"Could not load SIB-200 for {lang}: {e}")

    return samples_by_lang


def get_paired_samples(
    samples_by_lang: Dict[str, List[Dict]],
    reference_lang: str = "en"
) -> List[Tuple[Dict, str]]:
    """
    Create paired samples where each non-English sample is paired with its English equivalent.

    Returns list of (sample_dict, target_lang) tuples, where sample_dict contains
    both the target language version and the English version.
    """
    if reference_lang not in samples_by_lang:
        raise ValueError(f"Reference language {reference_lang} not in samples")

    ref_samples = {s["index"]: s for s in samples_by_lang[reference_lang]}
    paired = []

    for lang, samples in samples_by_lang.items():
        if lang == reference_lang:
            continue
        for sample in samples:
            if sample["index"] in ref_samples:
                paired_sample = {
                    "target": sample,
                    "reference": ref_samples[sample["index"]],
                    "target_lang": lang
                }
                paired.append((paired_sample, lang))

    return paired


if __name__ == "__main__":
    # Test loading
    print("Loading XNLI samples...")
    xnli_samples = load_xnli_samples(languages=["en", "de", "zh", "ar"], n_samples=5)
    for lang, samples in xnli_samples.items():
        print(f"\n{lang}: {len(samples)} samples")
        if samples:
            print(f"  Example: {samples[0]['premise'][:50]}...")

    print("\n\nLoading SIB-200 samples...")
    sib_samples = load_sib200_samples(languages=["en", "de", "zh"], n_samples=5)
    for lang, samples in sib_samples.items():
        print(f"\n{lang}: {len(samples)} samples")
        if samples:
            print(f"  Example: {samples[0]['text'][:50]}...")
