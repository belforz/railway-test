from langdetect import detect

def decide_language(text: str) -> str:
    try:
        idiom = detect(text)
        return idiom
    except Exception:
        return "pt"
    