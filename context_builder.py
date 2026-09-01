from typing import Any, List, Optional, Union
from data_service import (
    get_latest_workout,
    get_workout_history,
    get_movement_fingerprint,
    get_latest_report,
    get_rep_data,
)
from knowledge import APP_KNOWLEDGE


def _format_latest_workout(data: Optional[dict]) -> str:
    if not data:
        return "No recent workout data available."
    lines = [
        f"Exercise: {data.get('exercise', 'N/A')}",
        f"Date: {data.get('date', 'N/A')}",
        f"Total Reps: {data.get('total_reps', 'N/A')}",
        f"Average Score: {data.get('average_score', 'N/A')}/100",
        f"Best Rep: #{data.get('best_rep', 'N/A')} (Score: {data.get('best_score', 'N/A')})",
        f"Worst Rep: #{data.get('worst_rep', 'N/A')} (Score: {data.get('worst_score', 'N/A')})",
        f"Main Issue: {data.get('main_issue', 'N/A')}",
        f"Form Trend: {data.get('form_trend', 'N/A')}",
        f"Tempo Trend: {data.get('tempo_trend', 'N/A')}",
        f"Recommendation: {data.get('recommendation', 'N/A')}",
    ]
    return "\n".join(lines)


def _format_workout_history(data: Optional[List[dict]]) -> str:
    if not data:
        return "No workout history records available."
    lines = []
    for session in data:
        date = session.get("date", "Unknown Date")
        exercise = session.get("exercise", "Unknown Exercise")
        score = session.get("average_score", "N/A")
        volume = session.get("total_reps_or_duration", "N/A")
        issue = session.get("main_issue", "None noted")
        lines.append(f"- {date} | {exercise} | Score: {score} | Volume: {volume} | Primary Issue: {issue}")
    return "\n".join(lines)


def _format_movement_fingerprint(data: Optional[dict]) -> str:
    if not data:
        return "No movement fingerprint recorded yet."
    lines = []
    if "squat" in data:
        squat = data["squat"]
        lines.append(f"Squat Recurring Issue: {squat.get('recurring_issue', 'N/A')} (Frequency: {squat.get('frequency', 'N/A')})")
    if "plank" in data:
        plank = data["plank"]
        lines.append(f"Plank Recurring Issue: {plank.get('recurring_issue', 'N/A')} (Frequency: {plank.get('frequency', 'N/A')})")
    if "glute_bridge" in data:
        bridge = data["glute_bridge"]
        lines.append(f"Glute Bridge Stability Score: {bridge.get('stability_score', 'N/A')}/100")
    if "overall_biggest_recurring_issue" in data:
        lines.append(f"Overall Key Biomechanical Issue: {data['overall_biggest_recurring_issue']}")
    return "\n".join(lines)


def _format_latest_report(data: Optional[dict]) -> str:
    if not data:
        return "No workout report generated for this user."
    latest_workout = data.get("latest_workout", {})
    fingerprint = data.get("movement_fingerprint", {})

    report_lines = [
        "Session Summary:",
        f"- Exercise: {latest_workout.get('exercise', 'N/A')}",
        f"- Date: {latest_workout.get('date', 'N/A')}",
        f"- Score: {latest_workout.get('average_score', 'N/A')}/100",
        f"- Best Rep: #{latest_workout.get('best_rep', 'N/A')}, Worst Rep: #{latest_workout.get('worst_rep', 'N/A')}",
        f"- Main Issue: {latest_workout.get('main_issue', 'N/A')}",
        f"- Coach Recommendation: {latest_workout.get('recommendation', 'N/A')}",
    ]
    if fingerprint:
        report_lines.append(f"- Longitudinal Pattern: {fingerprint.get('overall_biggest_recurring_issue', 'N/A')}")
    return "\n".join(report_lines)


def _format_rep_data(data: Optional[List[dict]]) -> str:
    if not data:
        return "No individual repetition data available."
    lines = []
    for rep in data:
        rep_num = rep.get("rep_number", "N/A")
        score = rep.get("score", "N/A")
        issue = rep.get("detected_issue", "None")
        tempo = rep.get("tempo_seconds", "N/A")
        lines.append(f"Rep {rep_num}: Score {score}/100 | Tempo: {tempo}s | Issue: {issue}")
    return "\n".join(lines)


def _format_app_knowledge(data: Union[dict, str]) -> str:
    if isinstance(data, str):
        return data.strip()

    lines = [
        f"Supported Exercises: {', '.join(data.get('supported_exercises', []))}",
        "",
        "Camera Setup Guidance:",
        f"- Placement: {data.get('camera_setup_guidance', {}).get('placement', '')}",
        f"- Angle: {data.get('camera_setup_guidance', {}).get('angle', '')}",
        f"- Lighting: {data.get('camera_setup_guidance', {}).get('lighting', '')}",
        f"- Visibility: {data.get('camera_setup_guidance', {}).get('visibility', '')}",
        "",
        "Calibration:",
        f"- Purpose: {data.get('calibration', {}).get('purpose', '')}",
        f"- Process: {data.get('calibration', {}).get('process', '')}",
        "",
        "Scoring System:",
        f"- Scale: {data.get('scoring_system', {}).get('scale', '')}",
        f"- Components: {', '.join(data.get('scoring_system', {}).get('components', []))}",
        "",
        "Form Degradation Tracking:",
        f"- Definition: {data.get('form_degradation_tracking', {}).get('definition', '')}",
        f"- Indicators: {', '.join(data.get('form_degradation_tracking', {}).get('indicators', []))}",
        "",
        "Movement Fingerprint:",
        f"- Definition: {data.get('movement_fingerprint', {}).get('definition', '')}",
        f"- Purpose: {data.get('movement_fingerprint', {}).get('use_case', '')}",
    ]
    return "\n".join(lines)


def build_context(user_id: int, required_context: List[str]) -> str:
    """Fetch and assemble required context into a structured string for the LLM."""
    if not required_context:
        return ""

    sections = []

    if "latest_workout" in required_context:
        data = get_latest_workout(user_id)
        sections.append(f"=== LATEST WORKOUT ===\n{_format_latest_workout(data)}")

    if "workout_history" in required_context:
        data = get_workout_history(user_id)
        sections.append(f"=== WORKOUT HISTORY ===\n{_format_workout_history(data)}")

    if "movement_fingerprint" in required_context:
        data = get_movement_fingerprint(user_id)
        sections.append(f"=== MOVEMENT FINGERPRINT ===\n{_format_movement_fingerprint(data)}")

    if "latest_report" in required_context:
        data = get_latest_report(user_id)
        sections.append(f"=== LATEST REPORT ===\n{_format_latest_report(data)}")

    if "rep_data" in required_context:
        data = get_rep_data(user_id)
        sections.append(f"=== REP DATA ===\n{_format_rep_data(data)}")

    if "app_knowledge" in required_context:
        sections.append(f"=== APP KNOWLEDGE ===\n{_format_app_knowledge(APP_KNOWLEDGE)}")

    return "\n\n".join(sections)