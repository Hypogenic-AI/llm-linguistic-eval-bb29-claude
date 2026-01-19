# Research Plan: Evaluating Linguistic Performance in LLMs

## Motivation & Novelty Assessment

### Why This Research Matters
Large language models are increasingly being deployed at national scale in non-English-speaking countries (e.g., XAI's partnership with Venezuela, OpenAI with Estonia), yet these models are predominantly trained on English data. This creates a fundamental tension: end-users expect high-quality responses in their native languages, but models may internally process concepts through an English-centric lens. Understanding the extent of this bias and whether models employ implicit internal translation mechanisms is critical for:
1. **Equitable AI deployment**: Ensuring non-English speakers receive comparable service quality
2. **Model improvement**: Identifying where multilingual capabilities fall short
3. **Scientific understanding**: Illuminating how neural networks represent language and meaning

### Gap in Existing Work
Based on the literature review, several gaps exist:
1. **Limited empirical testing across LLM families**: Most studies focus on a single model (e.g., Llama-2) - we need comparative data across GPT, Claude, and other leading models
2. **Inconsistent methodology**: Studies use different datasets and metrics, making cross-comparison difficult
3. **API-based model opacity**: While Wendler et al. (2024) used mechanistic interpretability on open-source models, API-based models (GPT-4, Claude) cannot be analyzed at the layer level - but we can still measure their behavioral manifestations
4. **Language family analysis gaps**: Limited systematic comparison across language families (Indo-European, Sino-Tibetan, Afro-Asiatic, etc.)

### Our Novel Contribution
This research provides:
1. **Cross-model comparison**: First systematic comparison of multilingual performance across GPT-4.1, Claude Sonnet 4.5, and other 2024-2025 frontier models
2. **Behavioral evidence for internal translation**: Testing whether translating inputs to English before model processing improves non-English performance (if it does, models may already be doing this internally)
3. **Language family analysis**: Systematic breakdown of performance by language family and typological features
4. **Practical recommendations**: Actionable insights for deploying LLMs in multilingual contexts

### Experiment Justification

**Experiment 1: Cross-Language Performance Baseline**
- **Why needed?** Establishes the empirical foundation - we must first document the extent of English-centric bias across multiple state-of-the-art models
- **What we learn**: Quantifies performance gaps between English and other languages

**Experiment 2: Translate-to-English Strategy Testing**
- **Why needed?** Tests the implicit translation hypothesis behaviorally - if translating to English first improves performance, it suggests models internally process closer to English
- **What we learn**: Whether explicit translation compensates for English-centric training

**Experiment 3: Consistency Analysis Across Languages**
- **Why needed?** Checks if models give semantically equivalent responses across languages
- **What we learn**: Whether models access the same underlying "knowledge" regardless of input language

---

## Research Question
Do large language models trained predominantly on English data exhibit measurable performance disparities when deployed in non-English languages, and does explicit translation to English improve performance (suggesting implicit internal translation mechanisms)?

## Background and Motivation
LLMs are increasingly deployed globally, yet their training data is predominantly English. Wendler et al. (2024) showed that Llama-2 appears to use English as an internal "pivot language" - intermediate layers decode English tokens even for non-English inputs. This raises important questions about:
- How much worse do models perform on non-English tasks?
- Do frontier API models (GPT-4, Claude) exhibit similar English-centric behavior?
- Can explicit translation strategies mitigate performance gaps?

## Hypothesis Decomposition
**Main Hypothesis**: LLMs trained on predominantly English data underperform on non-English tasks and may possess implicit internal translation mechanisms.

**Sub-hypotheses**:
1. **H1**: LLMs achieve significantly higher accuracy on English inputs compared to equivalent inputs in other languages (performance gap hypothesis)
2. **H2**: Languages typologically distant from English (e.g., Sino-Tibetan, Afro-Asiatic) show larger performance gaps than closer languages (Indo-European)
3. **H3**: Translating non-English inputs to English before processing ("translate-test") improves model performance, suggesting models internally operate closer to English
4. **H4**: Different frontier models (GPT-4, Claude) exhibit similar patterns of English-centric bias

## Proposed Methodology

### Approach
We will evaluate multiple frontier LLMs on standardized multilingual benchmarks (XNLI, XCOPA, SIB-200), comparing:
1. Direct performance in each language
2. Performance with translate-to-English preprocessing
3. Cross-model consistency patterns

### Experimental Steps

**Step 1: Dataset Preparation**
- Load XNLI (15 languages) for natural language inference
- Load SIB-200 (8 languages) for topic classification
- Sample 100-200 examples per language for efficient API calls
- Rationale: These datasets have parallel test sets ensuring fair cross-language comparison

**Step 2: Baseline Evaluation (Direct Prompting)**
- Evaluate GPT-4.1, Claude Sonnet 4.5 on each language directly
- Use consistent prompting templates translated to target language
- Collect accuracy metrics
- Rationale: Establishes baseline performance in native language

**Step 3: Translate-Test Evaluation**
- Translate non-English inputs to English (using the models themselves)
- Re-evaluate on the translated versions
- Compare to direct performance
- Rationale: Tests whether explicit translation improves performance (supporting internal translation hypothesis)

**Step 4: Analysis by Language Family**
- Group languages by family (Indo-European, Sino-Tibetan, etc.)
- Compute performance gaps relative to English
- Test for correlation with linguistic distance
- Rationale: Tests whether typologically closer languages perform better

### Baselines
1. **Random baseline**: Expected accuracy for random guessing
2. **English performance**: Performance on English as upper bound
3. **Cross-model comparison**: GPT-4 vs Claude performance

### Evaluation Metrics
- **Accuracy**: Primary metric for classification tasks
- **Performance Gap (PG)**: (English accuracy - target language accuracy), measuring English-centric bias
- **Translate Gain (TG)**: (Translated performance - Direct performance), measuring whether translation helps
- **Confidence intervals**: Bootstrap 95% CI for all metrics

### Statistical Analysis Plan
- **Paired t-tests**: Compare English vs. other languages (within model)
- **One-way ANOVA**: Compare across language families
- **Correlation analysis**: Language distance vs. performance gap
- **Effect size**: Cohen's d for key comparisons
- **Significance level**: α = 0.05, with Bonferroni correction for multiple comparisons

## Expected Outcomes
1. **Supporting H1**: English accuracy > 10% higher than average non-English accuracy
2. **Supporting H2**: Indo-European languages show smaller gap than Sino-Tibetan/Afro-Asiatic
3. **Supporting H3**: Translate-test improves performance by > 5% for non-English languages
4. **Supporting H4**: Both GPT-4 and Claude show similar English-centric patterns

**Alternative outcomes**:
- If translate-test does NOT improve performance: Models may have learned genuine multilingual representations (not just English-centric)
- If non-Indo-European languages perform comparably: Models may be more multilingual than expected

## Timeline and Milestones
1. Environment setup and dataset preparation: 30 min
2. Implement evaluation pipeline: 60 min
3. Run baseline experiments: 60 min
4. Run translate-test experiments: 45 min
5. Statistical analysis and visualization: 45 min
6. Documentation and report writing: 30 min

## Potential Challenges
1. **API rate limits**: Mitigated by efficient batching and smaller sample sizes
2. **Translation quality**: Use same models for translation to keep conditions comparable
3. **Prompt sensitivity**: Test multiple prompt formats and report variance
4. **Cost management**: Sample ~100 examples per language to stay within budget

## Success Criteria
1. Clear documentation of performance gaps across languages
2. Statistical significance (p < 0.05) for key hypotheses
3. Interpretable visualizations showing language family patterns
4. Actionable insights about translate-test effectiveness
5. Reproducible code and methodology

---

## Implementation Details

### Models to Evaluate
1. **GPT-4.1** (OpenAI) - via API
2. **Claude Sonnet 4.5** (Anthropic) - via API

### Datasets
1. **XNLI** (15 languages): Natural language inference - entailment, contradiction, neutral
2. **SIB-200** (8 languages downloaded): Topic classification - 7 categories

### Languages by Family
- **Indo-European Germanic**: English (en), German (de)
- **Indo-European Romance**: French (fr), Spanish (es)
- **Indo-European Slavic**: Russian (ru), Bulgarian (bg)
- **Indo-European Indo-Iranian**: Hindi (hi), Urdu (ur)
- **Sino-Tibetan**: Chinese (zh)
- **Afro-Asiatic**: Arabic (ar)
- **Koreanic**: Korean (ko)
- **Japonic**: Japanese (ja)
- **Austroasiatic**: Vietnamese (vi)
- **Turkic**: Turkish (tr)
- **Niger-Congo**: Swahili (sw)
- **Tai-Kadai**: Thai (th)
- **Dravidian**: Tamil (ta)

### Sample Size Calculation
- Per language: 100 examples (sufficient for detecting 10% difference with 80% power)
- Total API calls estimate: ~1,500-2,000 (feasible within budget)
