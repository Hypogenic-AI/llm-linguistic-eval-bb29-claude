# Literature Review: Evaluating Linguistic Performance in LLMs

## Research Area Overview

This literature review examines research on multilingual capabilities of Large Language Models (LLMs), with a focus on: (1) the hypothesis that English-centric training leads to performance disparities across languages, (2) evidence for implicit internal translation mechanisms ("English as pivot language"), and (3) methods and benchmarks for evaluating cross-lingual performance.

The field has seen rapid growth, with key findings suggesting that LLMs trained predominantly on English data exhibit significant English-centric bias. Recent mechanistic interpretability work provides evidence that these models may internally represent concepts closer to English, even when processing non-English inputs.

---

## Key Papers

### Paper 1: Do Llamas Work in English? On the Latent Language of Multilingual Transformers
- **Authors**: Chris Wendler, Veniamin Veselovsky, Giovanni Monea, Robert West
- **Year**: 2024
- **Source**: arXiv:2402.10588
- **Key Contribution**: First empirical investigation of whether LLMs use English as an internal pivot language
- **Methodology**:
  - Applied "logit lens" technique to track intermediate embeddings through transformer layers
  - Analyzed Llama-2 family models with carefully constructed non-English prompts
  - Identified three distinct phases in forward pass processing
- **Key Findings**:
  - Middle layers decode semantically correct tokens in English before final layer outputs in target language
  - Three phases: (1) far from output embeddings, (2) English version decoded, (3) target language output
  - Evidence suggests abstract "concept space" lies closer to English than other languages
- **Code Available**: Yes - https://github.com/epfl-dlab/llm-latent-language
- **Relevance**: Directly addresses our hypothesis about implicit internal translation mechanisms

### Paper 2: Don't Trust ChatGPT when your Question is not in English
- **Authors**: Xiang Zhang, Senyu Li, Bradley Hauer, Ning Shi, Grzegorz Kondrak
- **Year**: 2023
- **Source**: arXiv:2305.16339
- **Key Contribution**: Systematic framework for categorizing and evaluating multilingual LLM abilities
- **Methodology**:
  - Proposed three bilingualism types for LLMs: compound, coordinate, subordinate
  - Introduced "Response Back-Translation" (RBT) method for evaluation
  - Categorized tasks into: Reasoning (least language impact), Knowledge Access, Articulation (most impact)
- **Key Findings**:
  - GPT achieves higher performance when tasks presented in English
  - Better performance on "translation-equivariant" tasks (correct output doesn't depend on input language)
  - LLMs exhibit mixture of coordinate and subordinate bilingualism
- **Datasets Used**: Multiple NLP benchmarks across languages
- **Relevance**: Provides framework for understanding how language choice affects LLM performance

### Paper 3: Is Translation All You Need? A Study on Solving Multilingual Tasks with LLMs
- **Authors**: Chaoqun Liu, Wenxuan Zhang, Yiran Zhao, Anh Tuan Luu, Lidong Bing
- **Year**: 2024
- **Source**: arXiv:2403.10258
- **Key Contribution**: Comprehensive evaluation of translation strategies for multilingual LLM tasks
- **Methodology**:
  - Compared translate-to-English approach vs. native language prompting
  - Evaluated on both NLP benchmarks and real-world user queries
  - Tested English-centric and non-English-centric LLMs
- **Key Findings**:
  - Translation to English improves performance on NLP tasks for English-centric LLMs
  - NOT universally optimal: culture-related tasks benefit from native language prompting
  - Non-English-centric LLMs behave differently from English-centric ones
- **Datasets Used**: MGSM, XCOPA, XNLI, PAWS-X, MKQA, XL-Sum (24 languages total)
- **Code Available**: Yes - https://github.com/DAMO-NLP-SG/translation-all-you-need
- **Relevance**: Directly tests whether translation is the optimal strategy for multilingual tasks

### Paper 4: XTREME: A Massively Multilingual Multi-task Benchmark
- **Authors**: Junjie Hu, Sebastian Ruder, Aditya Siddhant, Graham Neubig, et al.
- **Year**: 2020
- **Source**: arXiv:2003.11080 (ICML 2020)
- **Key Contribution**: First comprehensive multilingual benchmark covering 40 languages and 9 tasks
- **Methodology**:
  - Zero-shot cross-lingual transfer evaluation
  - Covers sentence classification, structured prediction, question answering, retrieval
  - Includes typologically diverse languages spanning 12 language families
- **Key Findings**:
  - Human performance achieved in English, but significant gap in other languages
  - Largest gaps for syntactic and sentence retrieval tasks
  - Performance varies widely: Indo-European languages perform better than Sino-Tibetan, Japonic, Koreanic, Niger-Congo
- **Baselines**: mBERT, XLM-R, machine translation approaches
- **Evaluation Metrics**: Task-specific (accuracy, F1, exact match, etc.)
- **Relevance**: Foundational benchmark for evaluating cross-lingual transfer

### Paper 5: SIB-200: A Simple, Inclusive, and Big Evaluation Dataset
- **Authors**: David Ifeoluwa Adelani, Hannah Liu, Xiaoyu Shen, et al.
- **Year**: 2023
- **Source**: arXiv:2309.07445
- **Key Contribution**: Topic classification benchmark covering 205 languages and dialects
- **Methodology**:
  - Based on Flores-200 machine translation corpus
  - Annotated English portion, extended to 204 other languages via parallel sentences
  - 7 topic categories: science/technology, travel, politics, sports, health, entertainment, geography
- **Key Findings**:
  - Large gap between high-resource and low-resource language performance
  - Languages unseen during pre-training, from under-represented families, and from Africa/Americas/Oceania/Southeast Asia have lowest performance
  - Scaling languages without scaling domains unhelpful (Glot-500 underperforms XLM-R)
- **Dataset Size**: 1,004 sentences per language (701 train, 99 dev, 204 test)
- **Code/Data Available**: https://github.com/dadelani/SIB-200
- **Relevance**: Largest NLU benchmark, good for testing hypothesis about low-resource languages

### Paper 6: BUFFET: Benchmarking Large Language Models for Few-shot Cross-lingual Transfer
- **Authors**: Akari Asai, Sneha Kudugunta, Xinyan Velocity Yu, et al.
- **Year**: 2023
- **Source**: arXiv:2305.14857
- **Key Contribution**: Few-shot cross-lingual transfer benchmark with 15 tasks across 54 languages
- **Methodology**:
  - Unified sequence-to-sequence format
  - Fixed few-shot examples (k=32) for fair comparison
  - Compared in-context learning vs. fine-tuning
- **Key Findings**:
  - ChatGPT with in-context learning often performs worse than smaller fine-tuned mT5 models
  - Instruction-tuned models struggle with few-shot samples
  - Significant room for improvement in few-shot cross-lingual transfer
- **Tasks**: NLI, paraphrase detection, sentiment analysis, QA, NER, summarization, etc.
- **Code/Data Available**: https://buffetfs.github.io/
- **Relevance**: Good for testing few-shot multilingual capabilities

### Paper 7: XLM-RoBERTa: Unsupervised Cross-lingual Representation Learning at Scale
- **Authors**: Alexis Conneau, Kartikay Khandelwal, Naman Goyal, et al.
- **Year**: 2019
- **Source**: arXiv:1911.02116
- **Key Contribution**: Foundational multilingual pre-trained model (100 languages)
- **Methodology**:
  - Trained on 2TB of filtered CommonCrawl data
  - Multilingual masked language modeling
- **Key Findings**:
  - Significant performance gains on cross-lingual transfer tasks
  - Outperformed previous multilingual models (mBERT)
- **Relevance**: Baseline model for multilingual evaluation

---

## Common Methodologies

### Evaluation Approaches
1. **Zero-shot cross-lingual transfer**: Train on English, evaluate on other languages (XTREME, XGLUE)
2. **Few-shot cross-lingual transfer**: Limited examples in target language (BUFFET)
3. **Translate-test**: Translate inputs to English, use English model (Liu et al., 2024)
4. **Mechanistic interpretability**: Logit lens to analyze internal representations (Wendler et al., 2024)

### Transfer Methods
- **Fine-tuning**: Train model parameters on task data
- **In-context learning (ICL)**: Provide examples in prompt without parameter updates
- **Multilingual adaptive fine-tuning (MAFT)**: Further pre-training on target language data

---

## Standard Baselines

| Model | Languages | Parameters | Notes |
|-------|-----------|------------|-------|
| mBERT | 104 | 110M | First widely-used multilingual encoder |
| XLM-R | 100 | 270M-3.5B | Strong baseline for cross-lingual tasks |
| mT5 | 101 | 300M-13B | Encoder-decoder, good for generation |
| BLOOM | 46 | Up to 176B | Open-source multilingual LLM |
| Llama-2 | ~20 | 7B-70B | English-centric but shows multilingual ability |

---

## Evaluation Metrics

- **Accuracy**: Classification tasks (topic classification, NLI)
- **F1 Score**: Token-level tasks (NER), QA (token overlap)
- **Exact Match (EM)**: Question answering
- **ROUGE-1/L**: Summarization and generation tasks
- **BLEU**: Translation-related tasks

---

## Datasets in the Literature

| Dataset | Languages | Task | Size | Source |
|---------|-----------|------|------|--------|
| XTREME | 40 | Multiple NLU | Varies | Multiple sources |
| SIB-200 | 205 | Topic classification | ~1K/lang | Flores-200 |
| BUFFET | 54 | 15 diverse tasks | Fixed k=32 | Multiple sources |
| MGSM | 10 | Math reasoning | 250/lang | Manually translated |
| XNLI | 15 | NLI | 5K/lang | MultiNLI translated |
| XCOPA | 11 | Commonsense | 1K/lang | COPA translated |
| MBBQ | 9 | Bias evaluation | ~2K/lang | BBQ translated |

---

## Gaps and Opportunities

### Current Gaps
1. **Mechanistic understanding**: Limited research on HOW models process non-English internally
2. **Low-resource languages**: Most benchmarks cover <100 languages; world has ~7,000
3. **Cultural knowledge**: Models may have cultural biases toward English-speaking cultures
4. **Domain coverage**: Pre-training often lacks domain diversity beyond web text

### Research Opportunities
1. **Testing English pivot hypothesis**: Use mechanistic interpretability to verify/quantify internal translation
2. **Cross-lingual knowledge consistency**: Do models give same answers in different languages?
3. **Language-specific vs. language-agnostic representations**: Where in the model are they separated?

---

## Recommendations for Our Experiment

### Recommended Datasets
1. **MGSM** (Multilingual Grade School Math): Tests reasoning with clear right/wrong answers across 10 languages
2. **SIB-200**: Topic classification across 205 languages, tests breadth
3. **XNLI/XCOPA**: NLU tasks with validated translations
4. **FLORES-200**: Parallel corpus for translation-based analysis

### Recommended Baselines
1. **Llama-2 (7B/13B)**: Primary subject for English pivot analysis
2. **XLM-R**: Strong multilingual encoder baseline
3. **mT5-base**: Encoder-decoder alternative
4. **GPT-4/Claude**: Comparison with proprietary models

### Recommended Metrics
1. **Accuracy** for classification tasks
2. **Performance gap** (English - target language) to quantify English bias
3. **Correlation with language resource size** to test low-resource hypothesis

### Methodological Considerations
1. **Control for translation quality**: Use human-translated test sets when available
2. **Language family analysis**: Group results by typological similarity
3. **Prompt language experiments**: Same task with prompts in different languages
4. **Layer-wise analysis**: Use logit lens to track when language-specific info emerges

---

## Key References

1. Wendler et al. (2024). "Do Llamas Work in English?" arXiv:2402.10588
2. Zhang et al. (2023). "Don't Trust ChatGPT when your Question is not in English" arXiv:2305.16339
3. Liu et al. (2024). "Is Translation All You Need?" arXiv:2403.10258
4. Hu et al. (2020). "XTREME: A Massively Multilingual Multi-task Benchmark" arXiv:2003.11080
5. Adelani et al. (2023). "SIB-200" arXiv:2309.07445
6. Asai et al. (2023). "BUFFET" arXiv:2305.14857
7. Conneau et al. (2019). "XLM-RoBERTa" arXiv:1911.02116
