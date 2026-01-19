"""Configuration for multilingual LLM evaluation experiments."""
import os
import random
import numpy as np

# Random seed for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Models to evaluate
MODELS = {
    "gpt-4.1": {"provider": "openai", "model_id": "gpt-4.1"},
    "claude-sonnet-4.5": {"provider": "openrouter", "model_id": "anthropic/claude-sonnet-4"},
}

# Dataset paths
DATASET_PATHS = {
    "xnli": "/data/hypogenicai/workspaces/llm-linguistic-eval-bb29-claude/datasets/xnli",
    "sib200": "/data/hypogenicai/workspaces/llm-linguistic-eval-bb29-claude/datasets/sib200",
}

# Output directories
RESULTS_DIR = "/data/hypogenicai/workspaces/llm-linguistic-eval-bb29-claude/results"
FIGURES_DIR = "/data/hypogenicai/workspaces/llm-linguistic-eval-bb29-claude/figures"

# Languages in XNLI
XNLI_LANGUAGES = [
    "en", "de", "fr", "es", "bg", "ru", "el", "hi", "ur",
    "ar", "zh", "vi", "th", "tr", "sw"
]

# Language families for analysis
LANGUAGE_FAMILIES = {
    "Indo-European/Germanic": ["en", "de"],
    "Indo-European/Romance": ["fr", "es"],
    "Indo-European/Slavic": ["bg", "ru"],
    "Indo-European/Greek": ["el"],
    "Indo-European/Indo-Iranian": ["hi", "ur"],
    "Afro-Asiatic": ["ar"],
    "Sino-Tibetan": ["zh"],
    "Austroasiatic": ["vi"],
    "Tai-Kadai": ["th"],
    "Turkic": ["tr"],
    "Niger-Congo": ["sw"],
}

# Reverse lookup: language -> family
LANGUAGE_TO_FAMILY = {}
for family, langs in LANGUAGE_FAMILIES.items():
    for lang in langs:
        LANGUAGE_TO_FAMILY[lang] = family

# Language full names
LANGUAGE_NAMES = {
    "en": "English", "de": "German", "fr": "French", "es": "Spanish",
    "bg": "Bulgarian", "ru": "Russian", "el": "Greek", "hi": "Hindi",
    "ur": "Urdu", "ar": "Arabic", "zh": "Chinese", "vi": "Vietnamese",
    "th": "Thai", "tr": "Turkish", "sw": "Swahili"
}

# NLI labels
NLI_LABELS = ["entailment", "neutral", "contradiction"]

# SIB-200 categories
SIB200_CATEGORIES = [
    "science/technology", "travel", "politics", "sports",
    "health", "entertainment", "geography"
]

# Sample sizes (per language for efficient API usage)
SAMPLE_SIZE_XNLI = 100  # 100 samples per language
SAMPLE_SIZE_SIB200 = 100  # 100 samples per language

# API settings
API_TEMPERATURE = 0.0  # Deterministic outputs
API_MAX_TOKENS = 50  # Short response for classification
API_TIMEOUT = 30  # seconds
