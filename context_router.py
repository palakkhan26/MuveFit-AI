import re
from typing import List


def detect_required_context(message: str) -> List[str]:
    """Analyze a user message using keyword and regex matching to determine required context sources."""
    if not message:
        return ["general_knowledge"]

    text = message.lower()
    sources: List[str] = []

    # 1. Safety Guidance
    safety_triggers = [
        "pain",
        "hurt",
        "injury",
        "injured",
        "stop exercising",
        "pause exercising",
        "safe to exercise",
        "doctor",
        "medical",
        "dizzy",
        "shortness of breath",
        "when should i pause",
        "should i stop",
    ]
    if any(k in text for k in safety_triggers):
        sources.append("safety_guidance")

    # 2. App Knowledge (camera, calibration, system mechanics)
    app_triggers = [
        "how does calibration",
        "calibration",
        "calibrate",
        "camera",
        "step back",
        "lighting",
        "placement",
        "muvefit work",
        "how muvefit",
        "app work",
        "supported exercise",
        "how does the app",
        "how does scoring work",
        "scoring system",
        "camera setup",
    ]
    if any(k in text for k in app_triggers):
        sources.append("app_knowledge")

    # 3. Latest Report
    report_triggers = [
        "report",
        "summary",
        "overview",
        "session breakdown",
        "latest report",
        "workout report",
    ]
    if any(k in text for k in report_triggers):
        sources.append("latest_report")

    # 4. Movement Fingerprint (recurring habits, persistent mistakes, tendencies)
    fingerprint_triggers = [
        "repeat",
        "repeating",
        "recurring",
        "habit",
        "fingerprint",
        "movement fingerprint",
        "always do wrong",
        "keep making",
        "keep doing",
        "tendency",
        "tendencies",
        "weakness",
        "usual mistake",
        "biggest issue",
        "most common mistake",
    ]
    if any(k in text for k in fingerprint_triggers):
        sources.append("movement_fingerprint")

    # 5. Workout History / Progress over time
    history_triggers = [
        "improve",
        "improved",
        "improvement",
        "progress",
        "history",
        "previous",
        "past workout",
        "last few",
        "over time",
        "compare",
        "trend",
        "last week",
        "sessions",
    ]
    if any(k in text for k in history_triggers):
        sources.append("workout_history")

    # 6. Rep Data (using word boundaries to avoid matching inside 'report' or 'repeat')
    rep_regex = r"\b(rep|reps|repetition|repetitions|worst rep|best rep|which rep|tempo|cadence|breakdown)\b"
    if re.search(rep_regex, text):
        sources.append("rep_data")

    # 7. Latest Workout
    latest_triggers = [
        "today",
        "latest",
        "last workout",
        "my workout",
        "my score",
        "score low",
        "score high",
        "my form",
        "just did",
        "recent",
        "this session",
        "worst rep",
        "best rep",
    ]
    if any(k in text for k in latest_triggers):
        sources.append("latest_workout")

    # If asking why the score was low on latest workout, include rep data
    if "score low" in text or "why was my score" in text or "what went wrong today" in text:
        if "rep_data" not in sources:
            sources.append("rep_data")
        if "latest_workout" not in sources:
            sources.append("latest_workout")

    # If asking about recurring mistakes, include history for comparative context
    if "movement_fingerprint" in sources and "workout_history" not in sources:
        sources.append("workout_history")

    # Deduplicate while preserving order
    deduped_sources: List[str] = []
    for s in sources:
        if s not in deduped_sources:
            deduped_sources.append(s)

    if not deduped_sources:
        return ["general_knowledge"]

    return deduped_sources