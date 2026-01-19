# Downloaded Datasets

This directory contains datasets for evaluating linguistic performance in LLMs across multiple languages. Data files are NOT committed to git due to size. Follow the download instructions below.

## Dataset Summary

| Dataset | Languages | Task | Size per Lang | Total Size |
|---------|-----------|------|---------------|------------|
| XNLI | 15 | Natural Language Inference | ~5K test | ~1GB |
| XCOPA | 11 | Commonsense Reasoning | 500 test | ~94KB |
| SIB-200 | 8 (downloaded) | Topic Classification | ~1K | ~1.5MB |

---

## Dataset 1: XNLI (Cross-lingual Natural Language Inference)

### Overview
- **Source**: HuggingFace `xnli` (all_languages config)
- **Size**: ~392K train, 5K test, 2.5K validation (15 languages)
- **Format**: HuggingFace Dataset
- **Task**: 3-way classification (entailment, contradiction, neutral)
- **Splits**: train, test, validation
- **License**: CC BY-NC 4.0

### Languages Covered
Arabic (ar), Bulgarian (bg), German (de), Greek (el), English (en), Spanish (es), French (fr), Hindi (hi), Russian (ru), Swahili (sw), Thai (th), Turkish (tr), Urdu (ur), Vietnamese (vi), Chinese (zh)

### Download Instructions

```python
from datasets import load_dataset

# Load all languages
xnli = load_dataset("xnli", "all_languages")
xnli.save_to_disk("datasets/xnli")
```

### Loading the Dataset

```python
from datasets import load_from_disk

xnli = load_from_disk("datasets/xnli")
print(xnli['test'][0])
# Output: {'premise': '...', 'hypothesis': '...', 'label': 0}
```

### Sample Data

```json
{
  "premise": "Conceptually cream skimming has two basic dimensions - product and geography.",
  "hypothesis": "Product and geography are what make cream skimming work.",
  "label": 1
}
```

### Notes
- Labels: 0=entailment, 1=neutral, 2=contradiction
- Good for testing cross-lingual understanding consistency

---

## Dataset 2: XCOPA (Cross-lingual Choice of Plausible Alternatives)

### Overview
- **Source**: HuggingFace `xcopa`
- **Size**: 100 validation, 500 test per language
- **Format**: HuggingFace Dataset
- **Task**: Binary choice commonsense reasoning
- **License**: CC BY 4.0

### Languages Covered
Estonian (et), Haitian Creole (ht), Indonesian (id), Italian (it), Quechua (qu), Swahili (sw), Tamil (ta), Thai (th), Turkish (tr), Vietnamese (vi), Chinese (zh)

### Download Instructions

```python
from datasets import load_dataset

# Download all languages
languages = ['et', 'ht', 'id', 'it', 'qu', 'sw', 'ta', 'th', 'tr', 'vi', 'zh']
for lang in languages:
    data = load_dataset("xcopa", lang)
    data.save_to_disk(f"datasets/xcopa/{lang}")
```

### Loading the Dataset

```python
from datasets import load_from_disk

xcopa_zh = load_from_disk("datasets/xcopa/zh")
print(xcopa_zh['test'][0])
```

### Sample Data (Chinese)

```json
{
  "premise": "那个女孩挥舞着魔棒。",
  "choice1": "乌鸦从帽子里飞了出来。",
  "choice2": "灰尘从帽子里飘了出来。",
  "question": "effect",
  "label": 0
}
```

### Notes
- Tests causal reasoning in different languages
- question: "cause" or "effect"
- label: 0 or 1 (index of correct choice)

---

## Dataset 3: SIB-200 (Simple, Inclusive, Big Evaluation)

### Overview
- **Source**: HuggingFace `Davlan/sib200`
- **Size**: 701 train, 99 validation, 204 test per language
- **Format**: HuggingFace Dataset
- **Task**: 7-way topic classification
- **License**: CC BY 4.0

### Categories
science/technology, travel, politics, sports, health, entertainment, geography

### Languages Downloaded
- eng_Latn (English)
- fra_Latn (French)
- zho_Hans (Chinese Simplified)
- spa_Latn (Spanish)
- deu_Latn (German)
- arb_Arab (Arabic)
- jpn_Jpan (Japanese)
- kor_Hang (Korean)

### Download Instructions

```python
from datasets import load_dataset

# Download any of the 205 available languages
lang_code = "eng_Latn"  # or fra_Latn, zho_Hans, etc.
sib200 = load_dataset("Davlan/sib200", lang_code)
sib200.save_to_disk(f"datasets/sib200/{lang_code}")
```

### Full Language List
See https://huggingface.co/datasets/Davlan/sib200 for all 205 languages

### Loading the Dataset

```python
from datasets import load_from_disk

sib200_en = load_from_disk("datasets/sib200/eng_Latn")
print(sib200_en['test'][0])
```

### Sample Data

```json
{
  "index_id": 431,
  "category": "geography",
  "text": "Turkey is encircled by seas on three sides: the Aegean Sea to the west, the Black Sea to the north and the Mediterranean Sea to the south."
}
```

### Notes
- Built on Flores-200 parallel corpus
- Same content across all languages (parallel text)
- Ideal for comparing performance across languages on identical content

---

## Recommendations for Experiments

### Primary Evaluation Tasks

1. **XNLI** - Test natural language inference across 15 languages
   - Metric: Accuracy
   - Compare English vs. other languages

2. **XCOPA** - Test commonsense reasoning
   - Metric: Accuracy
   - Tests diverse language families including low-resource

3. **SIB-200** - Test topic classification
   - Metric: Accuracy
   - 205 languages available for extensive coverage

### Suggested Experiment Design

1. **Baseline**: Evaluate LLM on English test sets
2. **Cross-lingual**: Evaluate same model on non-English test sets
3. **Performance Gap**: Calculate (English score - other language score)
4. **Analysis**: Correlate performance gap with:
   - Language resource size (high/mid/low resource)
   - Language family (Indo-European, Sino-Tibetan, etc.)
   - Script type (Latin, Cyrillic, Arabic, CJK, etc.)

### Language Groups for Analysis

**High-resource**: English, Chinese, Spanish, French, German
**Mid-resource**: Russian, Arabic, Hindi, Turkish, Vietnamese
**Low-resource**: Swahili, Haitian Creole, Quechua, Tamil

---

## Directory Structure

```
datasets/
├── .gitignore              # Excludes large files from git
├── README.md               # This file
├── xnli/                   # XNLI dataset (all languages)
│   ├── train/
│   ├── test/
│   ├── validation/
│   └── samples.json
├── xcopa/                  # XCOPA dataset
│   ├── zh/
│   └── samples.json
└── sib200/                 # SIB-200 topic classification
    ├── eng_Latn/
    ├── fra_Latn/
    ├── zho_Hans/
    ├── spa_Latn/
    ├── deu_Latn/
    ├── arb_Arab/
    ├── jpn_Jpan/
    └── kor_Hang/
```
