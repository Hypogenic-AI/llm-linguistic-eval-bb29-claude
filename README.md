# Multilingual LLM Evaluation: Cross-Lingual Performance Analysis

This repository contains code and results for evaluating linguistic performance gaps in Large Language Models across multiple languages.

## Research Question

Do LLMs trained predominantly on English data exhibit performance degradation on non-English languages? Is there evidence of implicit internal translation mechanisms?

## Key Findings

1. **English-centric bias confirmed**: Both GPT-4.1 and Claude Sonnet 4.5 show measurable performance drops on non-English languages (3.6% and 7.3% average gaps respectively)

2. **Translate-test effect**: Using English translations dramatically improves Claude's performance on non-Indo-European languages (up to +14.7% for Chinese/Arabic)

3. **Model differences**: GPT-4.1 shows more consistent cross-lingual performance; Claude excels in European languages but struggles with Asian/African languages

## Quick Start

```bash
# Set up environment
uv venv
source .venv/bin/activate
uv pip install datasets pandas numpy openai anthropic matplotlib seaborn scipy tqdm

# Configure API keys
export OPENAI_API_KEY="your-key"
export OPENROUTER_API_KEY="your-key"  # For Claude via OpenRouter

# Run evaluation
python src/evaluate.py --model gpt-4.1 --n-samples 75

# Analyze results
python src/analyze_results.py
```

## Project Structure

```
├── REPORT.md                 # Full research report with analysis
├── planning.md               # Experimental design document
├── src/
│   ├── config.py             # Configuration and constants
│   ├── data_loader.py        # XNLI dataset loading
│   ├── prompts.py            # Multilingual prompt templates
│   ├── llm_api.py            # OpenAI/Anthropic API wrapper
│   ├── evaluate.py           # Main evaluation script
│   └── analyze_results.py    # Analysis and visualization
├── results/
│   ├── results_gpt-4_1.json
│   ├── results_claude-sonnet-4_5.json
│   ├── statistics.txt
│   ├── summary_table.md
│   └── figures/              # Visualization outputs
├── datasets/
│   └── xnli/                 # XNLI benchmark data
└── literature_review.md      # Background research
```

## Languages Evaluated

| Language | Family | Script |
|----------|--------|--------|
| English | Indo-European (Germanic) | Latin |
| German | Indo-European (Germanic) | Latin |
| French | Indo-European (Romance) | Latin |
| Spanish | Indo-European (Romance) | Latin |
| Russian | Indo-European (Slavic) | Cyrillic |
| Hindi | Indo-European (Indo-Aryan) | Devanagari |
| Chinese | Sino-Tibetan | Han |
| Arabic | Afro-Asiatic (Semitic) | Arabic |
| Swahili | Niger-Congo (Bantu) | Latin |
| Turkish | Turkic | Latin |

## Results Summary

### Direct Evaluation Accuracy

| Model | English | Avg (non-EN) | Gap |
|-------|---------|--------------|-----|
| GPT-4.1 | 80.0% | 76.4% | 3.6% |
| Claude Sonnet 4.5 | 85.3% | 78.1% | 7.2% |

### Translate-Test Improvement (Claude)

| Language | Direct | Translate-Test | Change |
|----------|--------|----------------|--------|
| Chinese | 70.7% | 85.3% | +14.7% |
| Arabic | 70.7% | 85.3% | +14.7% |
| Swahili | 72.0% | 85.3% | +13.3% |
| Hindi | 73.3% | 85.3% | +12.0% |

## Citation

If you use this work, please cite:

```
@misc{multilingual-llm-eval-2026,
  title={Evaluating Linguistic Performance in LLMs: A Cross-Lingual Analysis},
  author={AI Research},
  year={2026},
  url={https://github.com/multilingual-llm-eval}
}
```

## License

MIT License
