def analyze_speech(text):

    filler_words = [
        "um",
        "uh",
        "like",
        "actually",
        "basically",
        "you know"
    ]

    words = text.lower().split()

    total_words = len(words)

    filler_count = sum(
        words.count(word)
        for word in filler_words
    )

    # Estimated Speech Duration (seconds)
    speech_duration = max(1, round(total_words / 2))

    # Words Per Minute
    wpm = int((total_words / speech_duration) * 60)

    # Confidence Score
    confidence_score = 100

    confidence_score -= filler_count * 5

    if wpm < 80:
        confidence_score -= 15

    elif wpm > 180:
        confidence_score -= 10

    confidence_score = max(
        0,
        min(100, confidence_score)
    )

    # Suggestions
    suggestions = []

    if filler_count > 0:
        suggestions.append(
            "Reduce filler words such as um, uh, like."
        )

    if wpm < 80:
        suggestions.append(
            "Try speaking slightly faster."
        )

    elif wpm > 180:
        suggestions.append(
            "Try speaking a little slower."
        )

    if confidence_score >= 85:
        suggestions.append(
            "Excellent confidence level."
        )

    elif confidence_score >= 70:
        suggestions.append(
            "Good confidence. Keep practicing."
        )

    else:
        suggestions.append(
            "Practice regularly to improve confidence."
        )

    return {
        "total_words": total_words,
        "filler_count": filler_count,
        "confidence_score": confidence_score,
        "wpm": wpm,
        "speech_duration": speech_duration,
        "suggestions": suggestions
    }