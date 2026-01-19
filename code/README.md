# Cloned Repositories

This directory contains code repositories relevant to evaluating linguistic performance in LLMs.

## Repositories

### 1. llm-latent-language
- **URL**: https://github.com/epfl-dlab/llm-latent-language
- **Paper**: "Do Llamas Work in English?" (Wendler et al., 2024)
- **Purpose**: Analysis of English as internal pivot language in LLMs using logit lens
- **Location**: `code/llm-latent-language/`
- **Key Files**:
  - `src/` - Main source code for experiments
  - `notebooks/` - Jupyter notebooks for analysis
  - `data/` - Data processing utilities
- **Requirements**: See `requirements.txt` in repo
- **Notes**: Core code for mechanistic interpretability analysis of multilingual processing

### 2. translation-all-you-need
- **URL**: https://github.com/DAMO-NLP-SG/translation-all-you-need
- **Paper**: "Is Translation All You Need?" (Liu et al., 2024)
- **Purpose**: Evaluation scripts for translate-to-English approach on multilingual tasks
- **Location**: `code/translation-all-you-need/`
- **Key Files**:
  - `scripts/` - Evaluation scripts
  - `prompts/` - Prompting templates for different languages
- **Requirements**: See `requirements.txt` in repo
- **Notes**: Good for testing translation hypothesis on NLP benchmarks

### 3. SIB-200
- **URL**: https://github.com/dadelani/SIB-200
- **Paper**: "SIB-200" (Adelani et al., 2023)
- **Purpose**: Evaluation code for topic classification across 205 languages
- **Location**: `code/sib-200/`
- **Key Files**:
  - `scripts/` - Training and evaluation scripts
  - `results/` - Baseline results
- **Requirements**: transformers, datasets
- **Notes**: Reference implementation for SIB-200 benchmark

### 4. XTREME
- **URL**: https://github.com/google-research/xtreme
- **Paper**: "XTREME" (Hu et al., 2020)
- **Purpose**: Massively multilingual benchmark evaluation code
- **Location**: `code/xtreme/`
- **Key Files**:
  - `scripts/` - Training scripts for all tasks
  - `third_party/` - Dataset loaders
  - `evaluate.py` - Main evaluation script
- **Requirements**: See `requirements.txt`
- **Notes**: Comprehensive evaluation framework for cross-lingual transfer

## Usage Notes

### Quick Start
1. Check each repository's `README.md` for specific setup instructions
2. Create a virtual environment before installing dependencies
3. Most repos require `transformers`, `datasets`, `torch` libraries

### Dependencies Installation
```bash
# General dependencies for all repos
pip install transformers datasets torch accelerate
```

### Adapting Code for Our Research

**For English-pivot analysis (llm-latent-language)**:
- Use logit lens code to analyze different LLMs
- Modify prompt templates for specific languages

**For translation experiments (translation-all-you-need)**:
- Scripts can be adapted for additional LLMs
- Prompting templates available for multiple languages

**For benchmark evaluation (SIB-200, XTREME)**:
- Standard evaluation scripts
- Can be extended to additional models
