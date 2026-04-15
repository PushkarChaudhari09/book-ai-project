def generate_summary(text):
    try:
        text = text.replace("...", ".")
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 10]

        if len(sentences) < 2:
            summary = text
        else:
            summary = ". ".join(sentences[:2]) + "."

        return summary

    except:
        return text


def classify_genre(text):
    text = text.lower()

    if "wizard" in text or "magic" in text:
        return "Fantasy"
    elif "love" in text or "romance" in text:
        return "Romance"
    elif "money" in text or "finance" in text:
        return "Finance"
    elif "crime" in text or "murder" in text:
        return "Thriller"
    elif "history" in text:
        return "Historical"
    else:
        return "General"