"""Prompt templates for multilingual LLM evaluation."""

# NLI task prompts - adapted for each language
NLI_PROMPTS = {
    "en": """Given a premise and a hypothesis, determine the relationship between them.

Premise: {premise}
Hypothesis: {hypothesis}

Choose exactly one: entailment, neutral, or contradiction.
Answer:""",

    "de": """Gegeben eine Prämisse und eine Hypothese, bestimmen Sie die Beziehung zwischen ihnen.

Prämisse: {premise}
Hypothese: {hypothesis}

Wählen Sie genau eines: entailment, neutral, oder contradiction.
Antwort:""",

    "fr": """Étant donné une prémisse et une hypothèse, déterminez la relation entre elles.

Prémisse: {premise}
Hypothèse: {hypothesis}

Choisissez exactement un: entailment, neutral, ou contradiction.
Réponse:""",

    "es": """Dada una premisa y una hipótesis, determine la relación entre ellas.

Premisa: {premise}
Hipótesis: {hypothesis}

Elija exactamente uno: entailment, neutral, o contradiction.
Respuesta:""",

    "bg": """Дадена е предпоставка и хипотеза, определете връзката между тях.

Предпоставка: {premise}
Хипотеза: {hypothesis}

Изберете точно едно: entailment, neutral, или contradiction.
Отговор:""",

    "ru": """Дана предпосылка и гипотеза, определите связь между ними.

Предпосылка: {premise}
Гипотеза: {hypothesis}

Выберите ровно одно: entailment, neutral, или contradiction.
Ответ:""",

    "el": """Δεδομένης μιας υπόθεσης και μιας υπόθεσης, προσδιορίστε τη σχέση μεταξύ τους.

Υπόθεση: {premise}
Υπόθεση: {hypothesis}

Επιλέξτε ακριβώς ένα: entailment, neutral, ή contradiction.
Απάντηση:""",

    "hi": """एक premise और एक hypothesis दिया गया है, उनके बीच संबंध निर्धारित करें।

Premise: {premise}
Hypothesis: {hypothesis}

बिल्कुल एक चुनें: entailment, neutral, या contradiction.
उत्तर:""",

    "ur": """ایک premise اور ایک hypothesis دی گئی ہے، ان کے درمیان تعلق کا تعین کریں۔

Premise: {premise}
Hypothesis: {hypothesis}

صرف ایک منتخب کریں: entailment، neutral، یا contradiction۔
جواب:""",

    "ar": """بالنظر إلى premise و hypothesis، حدد العلاقة بينهما.

Premise: {premise}
Hypothesis: {hypothesis}

اختر واحدة بالضبط: entailment أو neutral أو contradiction.
الإجابة:""",

    "zh": """给定一个前提和一个假设，确定它们之间的关系。

前提: {premise}
假设: {hypothesis}

请选择一个: entailment、neutral 或 contradiction。
答案:""",

    "vi": """Cho một tiền đề và một giả thuyết, xác định mối quan hệ giữa chúng.

Tiền đề: {premise}
Giả thuyết: {hypothesis}

Chọn chính xác một: entailment, neutral, hoặc contradiction.
Câu trả lời:""",

    "th": """กำหนดให้ premise และ hypothesis ให้ระบุความสัมพันธ์ระหว่างพวกเขา

Premise: {premise}
Hypothesis: {hypothesis}

เลือกอย่างใดอย่างหนึ่ง: entailment, neutral, หรือ contradiction
คำตอบ:""",

    "tr": """Bir önerme ve bir hipotez verildiğinde, aralarındaki ilişkiyi belirleyin.

Önerme: {premise}
Hipotez: {hypothesis}

Tam olarak birini seçin: entailment, neutral, veya contradiction.
Cevap:""",

    "sw": """Kwa premise na hypothesis zilizopewa, amua uhusiano kati yao.

Premise: {premise}
Hypothesis: {hypothesis}

Chagua moja kati ya: entailment, neutral, au contradiction.
Jibu:""",
}

# System prompts
NLI_SYSTEM_PROMPT = {
    "en": "You are a helpful assistant that classifies text relationships. Only respond with one word: entailment, neutral, or contradiction.",
    "multilingual": "You are a helpful assistant. Respond only with: entailment, neutral, or contradiction."
}

# Topic classification prompts for SIB-200
TOPIC_PROMPTS = {
    "en": """Classify the following text into one of these categories:
- science/technology
- travel
- politics
- sports
- health
- entertainment
- geography

Text: {text}

Category:""",
}

TOPIC_SYSTEM_PROMPT = "You are a text classifier. Respond with only the category name, nothing else."

# Translation prompts (for translate-test approach)
TRANSLATION_PROMPT = """Translate the following text to English, preserving the meaning exactly.

Text: {text}

English translation:"""


def format_nli_prompt(premise: str, hypothesis: str, language: str = "en") -> str:
    """Format an NLI prompt for the given language."""
    template = NLI_PROMPTS.get(language, NLI_PROMPTS["en"])
    return template.format(premise=premise, hypothesis=hypothesis)


def format_topic_prompt(text: str, language: str = "en") -> str:
    """Format a topic classification prompt."""
    template = TOPIC_PROMPTS.get(language, TOPIC_PROMPTS["en"])
    return template.format(text=text)


def format_translation_prompt(text: str) -> str:
    """Format a translation prompt."""
    return TRANSLATION_PROMPT.format(text=text)


def parse_nli_response(response: str) -> str:
    """Parse NLI response to extract label."""
    response_lower = response.lower().strip()

    # Look for exact matches first
    for label in ["entailment", "neutral", "contradiction"]:
        if label in response_lower:
            return label

    # Check for partial matches
    if "entail" in response_lower:
        return "entailment"
    if "neutr" in response_lower:
        return "neutral"
    if "contrad" in response_lower:
        return "contradiction"

    # Default to neutral if unclear
    return "neutral"


def parse_topic_response(response: str) -> str:
    """Parse topic classification response."""
    response_lower = response.lower().strip()

    categories = [
        "science/technology", "travel", "politics", "sports",
        "health", "entertainment", "geography"
    ]

    for cat in categories:
        if cat in response_lower:
            return cat

    # Partial matches
    if "science" in response_lower or "technology" in response_lower or "tech" in response_lower:
        return "science/technology"
    if "travel" in response_lower:
        return "travel"
    if "politic" in response_lower:
        return "politics"
    if "sport" in response_lower:
        return "sports"
    if "health" in response_lower:
        return "health"
    if "entertainment" in response_lower:
        return "entertainment"
    if "geography" in response_lower or "geo" in response_lower:
        return "geography"

    return response_lower
