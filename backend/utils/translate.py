from deep_translator import GoogleTranslator


def translate(text: str):
    return GoogleTranslator(
        source="auto", target="pt").translate(text)
