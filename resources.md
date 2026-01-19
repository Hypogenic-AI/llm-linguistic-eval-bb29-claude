# Resources Catalog

This document catalogs all resources gathered for the research project on evaluating linguistic performance in LLMs.

## Summary

| Resource Type | Count | Description |
|--------------|-------|-------------|
| Papers | 10 | Academic papers on multilingual LLM evaluation |
| Datasets | 3 | Multilingual NLU benchmarks |
| Code Repos | 4 | Implementation and evaluation code |

---

## Papers

Total papers downloaded: **10**

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Do Llamas Work in English? | Wendler et al. | 2024 | papers/2402.10588_llamas_english_pivot.pdf | English pivot language analysis |
| Don't Trust ChatGPT when not in English | Zhang et al. | 2023 | papers/2305.16339_dont_trust_chatgpt_non_english.pdf | Bilingualism typology for LLMs |
| Is Translation All You Need? | Liu et al. | 2024 | papers/2403.10258_translation_multilingual.pdf | Translation strategy evaluation |
| XTREME Benchmark | Hu et al. | 2020 | papers/2003.11080_xtreme_benchmark.pdf | Foundational multilingual benchmark |
| SIB-200 | Adelani et al. | 2023 | papers/2309.07445_sib200.pdf | 205-language topic classification |
| BUFFET | Asai et al. | 2023 | papers/2305.14857_buffet.pdf | Few-shot cross-lingual benchmark |
| XLM-RoBERTa | Conneau et al. | 2019 | papers/1911.02116_xlm_roberta.pdf | Foundational multilingual model |
| Multilingual LLM Survey | Xu et al. | 2024 | papers/2403.03887_multilingual_llm_survey.pdf | Comprehensive MLLM survey |
| MBBQ Cross-lingual Bias | Neplenbroek et al. | 2024 | papers/2406.18902_mbbq_crosslingual_bias.pdf | Cross-lingual bias evaluation |
| MEXA Multilingual Evaluation | Kargaran et al. | 2024 | papers/2407.02797_mexa_multilingual.pdf | English-centric LLM evaluation |

See `papers/README.md` for detailed descriptions of each paper.

---

## Datasets

Total datasets downloaded: **3** (with multiple language variants)

| Name | Source | Languages | Task | Location | Notes |
|------|--------|-----------|------|----------|-------|
| XNLI | HuggingFace | 15 | NLI | datasets/xnli/ | Natural language inference |
| XCOPA | HuggingFace | 11 | Reasoning | datasets/xcopa/ | Commonsense reasoning |
| SIB-200 | HuggingFace | 8 (205 available) | Classification | datasets/sib200/ | Topic classification |

### Language Coverage

**XNLI** (15 languages):
- High-resource: English, Chinese, Spanish, French, German
- Mid-resource: Russian, Arabic, Hindi, Turkish, Vietnamese
- Low-resource: Swahili, Thai, Greek, Bulgarian, Urdu

**XCOPA** (11 languages):
- European: Estonian, Italian
- Asian: Thai, Vietnamese, Chinese, Tamil, Indonesian
- Other: Swahili, Turkish, Haitian Creole, Quechua

**SIB-200** (8 downloaded, 205 available):
- Downloaded: English, French, Chinese, Spanish, German, Arabic, Japanese, Korean
- Note: Can download any of 205 languages as needed

See `datasets/README.md` for download instructions and detailed descriptions.

---

## Code Repositories

Total repositories cloned: **4**

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| llm-latent-language | github.com/epfl-dlab/llm-latent-language | English pivot analysis | code/llm-latent-language/ | Logit lens implementation |
| translation-all-you-need | github.com/DAMO-NLP-SG/translation-all-you-need | Translation evaluation | code/translation-all-you-need/ | Translate-test scripts |
| SIB-200 | github.com/dadelani/SIB-200 | Classification benchmark | code/sib-200/ | Baseline implementation |
| XTREME | github.com/google-research/xtreme | Multilingual benchmark | code/xtreme/ | Comprehensive evaluation |

See `code/README.md` for detailed descriptions and usage instructions.

---

## Resource Gathering Notes

### Search Strategy
1. Used paper-finder service for initial literature search with queries on:
   - "multilingual LLM evaluation cross-lingual performance English-centric bias"
   - "cross-lingual transfer learning language models benchmark dataset"
   - "implicit translation LLM internal language representation multilingual"
2. Downloaded papers from arXiv based on relevance scores
3. Identified datasets from papers and HuggingFace
4. Cloned repositories linked from papers

### Selection Criteria
- **Papers**: Selected based on relevance to research hypothesis (English-centric bias, internal translation mechanisms)
- **Datasets**: Focused on multilingual benchmarks with parallel text or consistent task across languages
- **Code**: Prioritized implementations directly related to our research questions

### Challenges Encountered
1. Some arXiv IDs from paper-finder pointed to wrong papers (different papers with same ID)
2. Flores-200 dataset no longer available via HuggingFace datasets library (scripts deprecated)
3. MGSM dataset requires custom loading (scripts deprecated)

### Gaps and Workarounds
1. **Flores-200**: Used SIB-200 instead (built on Flores-200 parallel corpus)
2. **MGSM**: Can be loaded manually from original source if needed for math reasoning evaluation
3. **Missing "Do Multilingual LLMs Think In English?" paper**: Related findings covered by "Do Llamas Work in English?" paper

---

## Recommendations for Experiment Design

Based on gathered resources, we recommend:

### 1. Primary Dataset(s)
- **XNLI**: Well-established NLI benchmark, 15 diverse languages
- **SIB-200**: Large language coverage (205), parallel text for fair comparison
- **XCOPA**: Commonsense reasoning with low-resource languages

### 2. Baseline Methods
- **Zero-shot prompting**: Direct evaluation in target language
- **Translate-test**: Translate input to English, evaluate, translate back
- **Few-shot in-context learning**: k=5-32 examples

### 3. Evaluation Metrics
- **Accuracy**: Primary metric for classification tasks
- **Performance Gap**: (English accuracy - target language accuracy)
- **Language-family analysis**: Group by Indo-European, Sino-Tibetan, etc.

### 4. Code to Adapt/Reuse
- `llm-latent-language`: For mechanistic analysis of English pivot hypothesis
- `translation-all-you-need`: For implementing translate-test baseline
- `xtreme`: For standardized evaluation scripts

### 5. Suggested Experimental Setup

**Phase 1: Baseline Establishment**
- Evaluate LLMs on XNLI (15 languages) and SIB-200 (8 languages)
- Document English vs. other language performance

**Phase 2: Translation Hypothesis Testing**
- Apply translate-to-English approach
- Compare direct vs. translated performance
- Analyze which language types benefit most

**Phase 3: Internal Mechanism Analysis**
- Use logit lens to analyze layer-wise language representations
- Track when English tokens appear in intermediate layers
- Correlate with downstream performance

---

## Quick Reference

### File Locations
```
papers/           - Downloaded PDF papers
datasets/         - Downloaded datasets (HuggingFace format)
code/             - Cloned repositories
literature_review.md - Comprehensive literature synthesis
resources.md      - This file
```

### Key Commands

**Load XNLI dataset:**
```python
from datasets import load_from_disk
xnli = load_from_disk("datasets/xnli")
```

**Load SIB-200 (English):**
```python
from datasets import load_from_disk
sib = load_from_disk("datasets/sib200/eng_Latn")
```

**Load XCOPA (Chinese):**
```python
from datasets import load_from_disk
xcopa = load_from_disk("datasets/xcopa/zh")
```

---

## References

Full bibliography available in `literature_review.md`.
