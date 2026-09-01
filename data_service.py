import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# Supports demo_user_data.json in the same directory or in a ./data subfolder
CURRENT_DIR = Path(__file__).resolve().parent
DATA_PATH = CURRENT_DIR / "demo_user_data.json"
ALT_DATA_PATH = CURRENT_DIR / "data" / "demo_user_data.json"


def _load_raw_data() -> Optional[Any]:
  """Safely read and parse the demo JSON file."""
  target_file = None
  if DATA_PATH.is_file():
    target_file = DATA_PATH
  elif ALT_DATA_PATH.is_file():
    target_file = ALT_DATA_PATH
  else:
    return None

  try:
    with open(target_file, "r", encoding="utf-8") as file:
      return json.load(file)
  except (json.JSONDecodeError, OSError):
    return None


def _get_user_record(user_id: int) -> Optional[Dict[str, Any]]:
  """Retrieve data corresponding to the given user_id."""
  data = _load_raw_data()
  if data is None:
    return None

  # Handle a list of user objects
  if isinstance(data, list):
    for user in data:
      if isinstance(user, dict) and user.get("user_id") == user_id:
        return user
    return None

  # Handle a single user object
  if isinstance(data, dict):
    if data.get("user_id") == user_id:
      return data

  return None


def get_latest_workout(user_id: int) -> Optional[Dict[str, Any]]:
  """Return the latest workout for the given user_id."""
  user = _get_user_record(user_id)
  if not user:
    return None
  return user.get("latest_workout")


def get_workout_history(user_id: int) -> Optional[List[Dict[str, Any]]]:
  """Return the workout history for the given user_id."""
  user = _get_user_record(user_id)
  if not user:
    return None
  return user.get("workout_history")


def get_movement_fingerprint(user_id: int) -> Optional[Dict[str, Any]]:
  """Return the movement fingerprint for the given user_id."""
  user = _get_user_record(user_id)
  if not user:
    return None
  return user.get("movement_fingerprint")


def get_latest_report(user_id: int) -> Optional[Dict[str, Any]]:
  """Return an aggregated latest session summary report for the given user_id."""
  user = _get_user_record(user_id)
  if not user:
    return None

  latest_workout = user.get("latest_workout")
  if not latest_workout:
    return None

  return {
      "user_id": user_id,
      "latest_workout": latest_workout,
      "movement_fingerprint": user.get("movement_fingerprint"),
  }


def get_rep_data(user_id: int) -> Optional[List[Dict[str, Any]]]:
  """Return the detailed repetition-level data for the given user_id."""
  user = _get_user_record(user_id)
  if not user:
    return None
  return user.get("rep_data")