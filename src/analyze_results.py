"""Analyze and visualize multilingual LLM evaluation results."""
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configure plotting
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Directories
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Language metadata
LANGUAGE_FAMILIES = {
    "en": "Indo-European (Germanic)",
    "de": "Indo-European (Germanic)",
    "fr": "Indo-European (Romance)",
    "es": "Indo-European (Romance)",
    "ru": "Indo-European (Slavic)",
    "hi": "Indo-European (Indo-Aryan)",
    "ar": "Afro-Asiatic (Semitic)",
    "zh": "Sino-Tibetan",
    "sw": "Niger-Congo (Bantu)",
    "tr": "Turkic"
}

LANGUAGE_NAMES = {
    "en": "English", "de": "German", "fr": "French", "es": "Spanish",
    "zh": "Chinese", "ar": "Arabic", "sw": "Swahili", "hi": "Hindi",
    "ru": "Russian", "tr": "Turkish"
}


def load_results():
    """Load all results files."""
    results = {}
    for filename in os.listdir(RESULTS_DIR):
        if filename.startswith("results_") and filename.endswith(".json"):
            filepath = os.path.join(RESULTS_DIR, filename)
            with open(filepath) as f:
                data = json.load(f)
                model = data.get("model", filename.replace("results_", "").replace(".json", ""))
                results[model] = data
    return results


def compute_performance_gaps(results):
    """Calculate performance gaps between English and other languages."""
    gaps = {}
    for model, data in results.items():
        if "direct" not in data:
            continue
        english_acc = data["direct"].get("en", {}).get("accuracy", 0)
        gaps[model] = {}
        for lang, lang_data in data["direct"].items():
            if lang != "en":
                gaps[model][lang] = english_acc - lang_data.get("accuracy", 0)
    return gaps


def compute_translate_test_effect(results):
    """Calculate improvement from translate-test approach."""
    effects = {}
    for model, data in results.items():
        if "direct" not in data or "translate_test" not in data:
            continue
        effects[model] = {}
        for lang in data["translate_test"]:
            direct_acc = data["direct"].get(lang, {}).get("accuracy", 0)
            translate_acc = data["translate_test"][lang].get("accuracy", 0)
            effects[model][lang] = translate_acc - direct_acc
    return effects


def plot_accuracy_comparison(results):
    """Create bar chart comparing accuracy across languages."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    models = list(results.keys())
    languages = ["en", "de", "fr", "es", "zh", "ar", "sw", "hi", "ru", "tr"]

    for idx, model in enumerate(models):
        ax = axes[idx]
        data = results[model]

        direct_accs = [data["direct"].get(lang, {}).get("accuracy", 0) * 100 for lang in languages]
        translate_accs = [
            data["translate_test"].get(lang, {}).get("accuracy", 0) * 100
            if lang != "en" else data["direct"].get("en", {}).get("accuracy", 0) * 100
            for lang in languages
        ]

        x = np.arange(len(languages))
        width = 0.35

        bars1 = ax.bar(x - width/2, direct_accs, width, label='Direct', color='steelblue')
        bars2 = ax.bar(x + width/2, translate_accs, width, label='Translate-Test', color='coral')

        ax.set_xlabel('Language')
        ax.set_ylabel('Accuracy (%)')
        ax.set_title(f'{model.replace("-", " ").title()}')
        ax.set_xticks(x)
        ax.set_xticklabels([LANGUAGE_NAMES.get(l, l) for l in languages], rotation=45, ha='right')
        ax.legend()
        ax.set_ylim(60, 100)
        ax.axhline(y=data["direct"].get("en", {}).get("accuracy", 0) * 100,
                   color='gray', linestyle='--', alpha=0.5, label='English baseline')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "accuracy_comparison.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: accuracy_comparison.png")


def plot_performance_gap_heatmap(results):
    """Create heatmap showing performance gaps."""
    gaps = compute_performance_gaps(results)

    models = list(gaps.keys())
    languages = ["de", "fr", "es", "zh", "ar", "sw", "hi", "ru", "tr"]

    gap_matrix = []
    for model in models:
        row = [gaps[model].get(lang, 0) * 100 for lang in languages]
        gap_matrix.append(row)

    gap_matrix = np.array(gap_matrix)

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(gap_matrix, annot=True, fmt='.1f', cmap='RdYlGn_r',
                xticklabels=[LANGUAGE_NAMES.get(l, l) for l in languages],
                yticklabels=models, ax=ax, center=0,
                cbar_kws={'label': 'Performance Gap (% points)'})
    ax.set_title('Performance Gap: English - Target Language (Direct Evaluation)')
    ax.set_xlabel('Target Language')
    ax.set_ylabel('Model')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "performance_gap_heatmap.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: performance_gap_heatmap.png")


def plot_translate_test_effect(results):
    """Create chart showing translate-test effect."""
    effects = compute_translate_test_effect(results)

    models = list(effects.keys())
    languages = ["de", "fr", "es", "zh", "ar", "sw", "hi", "ru", "tr"]

    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(languages))
    width = 0.35

    for idx, model in enumerate(models):
        model_effects = [effects[model].get(lang, 0) * 100 for lang in languages]
        offset = (idx - len(models)/2 + 0.5) * width
        bars = ax.bar(x + offset, model_effects, width, label=model)

        # Add value labels
        for i, v in enumerate(model_effects):
            ax.text(i + offset, v + 0.5 if v > 0 else v - 1.5, f'{v:.1f}',
                   ha='center', va='bottom' if v > 0 else 'top', fontsize=8)

    ax.set_xlabel('Language')
    ax.set_ylabel('Accuracy Change (% points)')
    ax.set_title('Effect of Translate-Test Approach (Translate-Test − Direct)')
    ax.set_xticks(x)
    ax.set_xticklabels([LANGUAGE_NAMES.get(l, l) for l in languages], rotation=45, ha='right')
    ax.legend()
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "translate_test_effect.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: translate_test_effect.png")


def plot_language_family_analysis(results):
    """Analyze performance by language family."""
    # Group languages by family
    family_groups = {}
    for lang, family in LANGUAGE_FAMILIES.items():
        if family not in family_groups:
            family_groups[family] = []
        family_groups[family].append(lang)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for idx, (model, data) in enumerate(results.items()):
        ax = axes[idx]

        families = []
        avg_accs = []
        std_accs = []

        for family, langs in sorted(family_groups.items()):
            accs = []
            for lang in langs:
                if lang in data["direct"]:
                    accs.append(data["direct"][lang]["accuracy"] * 100)
            if accs:
                families.append(family.split(" (")[0])  # Shorten name
                avg_accs.append(np.mean(accs))
                std_accs.append(np.std(accs) if len(accs) > 1 else 0)

        colors = plt.cm.tab10(np.linspace(0, 1, len(families)))
        bars = ax.barh(families, avg_accs, xerr=std_accs, capsize=3, color=colors)

        ax.set_xlabel('Accuracy (%)')
        ax.set_title(f'{model.replace("-", " ").title()} - By Language Family')
        ax.set_xlim(60, 100)

        # Add value labels
        for bar, acc in zip(bars, avg_accs):
            ax.text(acc + 1, bar.get_y() + bar.get_height()/2, f'{acc:.1f}%',
                   va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "language_family_analysis.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: language_family_analysis.png")


def plot_model_comparison_radar(results):
    """Create radar chart comparing models across languages."""
    languages = ["en", "de", "fr", "es", "zh", "ar", "sw", "hi", "ru", "tr"]
    n_langs = len(languages)

    # Create angles for radar chart
    angles = np.linspace(0, 2 * np.pi, n_langs, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    colors = ['steelblue', 'coral']
    for idx, (model, data) in enumerate(results.items()):
        values = [data["direct"].get(lang, {}).get("accuracy", 0) * 100 for lang in languages]
        values += values[:1]  # Complete the loop

        ax.plot(angles, values, 'o-', linewidth=2, label=model, color=colors[idx])
        ax.fill(angles, values, alpha=0.1, color=colors[idx])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([LANGUAGE_NAMES.get(l, l) for l in languages])
    ax.set_ylim(60, 100)
    ax.set_title('Model Performance Comparison Across Languages', y=1.08)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "model_comparison_radar.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: model_comparison_radar.png")


def compute_statistics(results):
    """Compute statistical analysis of results."""
    stats_report = []
    stats_report.append("=" * 60)
    stats_report.append("STATISTICAL ANALYSIS")
    stats_report.append("=" * 60)

    # Extract accuracies
    for model, data in results.items():
        stats_report.append(f"\n{model}")
        stats_report.append("-" * 40)

        direct_accs = [v["accuracy"] for v in data["direct"].values()]
        stats_report.append(f"Direct Evaluation:")
        stats_report.append(f"  Mean: {np.mean(direct_accs)*100:.2f}%")
        stats_report.append(f"  Std:  {np.std(direct_accs)*100:.2f}%")
        stats_report.append(f"  Min:  {np.min(direct_accs)*100:.2f}%")
        stats_report.append(f"  Max:  {np.max(direct_accs)*100:.2f}%")

        # Non-English languages
        non_en_accs = [v["accuracy"] for k, v in data["direct"].items() if k != "en"]
        en_acc = data["direct"]["en"]["accuracy"]
        stats_report.append(f"\nEnglish vs Non-English:")
        stats_report.append(f"  English:     {en_acc*100:.2f}%")
        stats_report.append(f"  Non-English: {np.mean(non_en_accs)*100:.2f}% (mean)")
        stats_report.append(f"  Gap:         {(en_acc - np.mean(non_en_accs))*100:.2f}%")

        # Translate-test analysis
        if "translate_test" in data:
            improvements = []
            for lang in data["translate_test"]:
                direct = data["direct"].get(lang, {}).get("accuracy", 0)
                translate = data["translate_test"][lang]["accuracy"]
                improvements.append(translate - direct)

            stats_report.append(f"\nTranslate-Test Effect:")
            stats_report.append(f"  Mean improvement: {np.mean(improvements)*100:.2f}%")
            stats_report.append(f"  Languages improved: {sum(1 for i in improvements if i > 0)}/{len(improvements)}")

    # Cross-model comparison
    models = list(results.keys())
    if len(models) == 2:
        stats_report.append("\n" + "=" * 60)
        stats_report.append("CROSS-MODEL COMPARISON")
        stats_report.append("=" * 60)

        for lang in results[models[0]]["direct"]:
            acc1 = results[models[0]]["direct"][lang]["accuracy"]
            acc2 = results[models[1]]["direct"][lang]["accuracy"]
            diff = (acc2 - acc1) * 100
            winner = models[1] if diff > 0 else models[0]
            stats_report.append(f"{LANGUAGE_NAMES.get(lang, lang):10s}: {models[0]}={acc1*100:.1f}%, {models[1]}={acc2*100:.1f}% (Δ={diff:+.1f}%, {winner})")

    return "\n".join(stats_report)


def generate_summary_table(results):
    """Generate markdown summary table."""
    languages = ["en", "de", "fr", "es", "zh", "ar", "sw", "hi", "ru", "tr"]

    table = []
    table.append("## Results Summary\n")

    # Direct evaluation table
    table.append("### Direct Evaluation Accuracy\n")
    header = "| Language | " + " | ".join(results.keys()) + " |"
    separator = "|----------|" + "|".join(["-------" for _ in results]) + "|"
    table.append(header)
    table.append(separator)

    for lang in languages:
        row = f"| {LANGUAGE_NAMES.get(lang, lang)} |"
        for model, data in results.items():
            acc = data["direct"].get(lang, {}).get("accuracy", 0) * 100
            row += f" {acc:.1f}% |"
        table.append(row)

    # Average
    row = "| **Average** |"
    for model, data in results.items():
        accs = [v["accuracy"] for v in data["direct"].values()]
        row += f" **{np.mean(accs)*100:.1f}%** |"
    table.append(row)

    # Translate-test table
    table.append("\n### Translate-Test Effect (Change in Accuracy)\n")
    header = "| Language | " + " | ".join(results.keys()) + " |"
    table.append(header)
    table.append(separator)

    for lang in languages:
        if lang == "en":
            continue
        row = f"| {LANGUAGE_NAMES.get(lang, lang)} |"
        for model, data in results.items():
            direct = data["direct"].get(lang, {}).get("accuracy", 0)
            translate = data["translate_test"].get(lang, {}).get("accuracy", 0)
            diff = (translate - direct) * 100
            sign = "+" if diff > 0 else ""
            row += f" {sign}{diff:.1f}% |"
        table.append(row)

    return "\n".join(table)


def main():
    """Run full analysis."""
    print("Loading results...")
    results = load_results()

    if not results:
        print("No results found!")
        return

    print(f"Found {len(results)} models: {list(results.keys())}")

    # Generate visualizations
    print("\nGenerating visualizations...")
    plot_accuracy_comparison(results)
    plot_performance_gap_heatmap(results)
    plot_translate_test_effect(results)
    plot_language_family_analysis(results)
    plot_model_comparison_radar(results)

    # Compute statistics
    print("\nComputing statistics...")
    stats_report = compute_statistics(results)
    print(stats_report)

    # Save statistics
    stats_path = os.path.join(RESULTS_DIR, "statistics.txt")
    with open(stats_path, "w") as f:
        f.write(stats_report)
    print(f"\nSaved: {stats_path}")

    # Generate summary table
    summary = generate_summary_table(results)
    summary_path = os.path.join(RESULTS_DIR, "summary_table.md")
    with open(summary_path, "w") as f:
        f.write(summary)
    print(f"Saved: {summary_path}")

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
