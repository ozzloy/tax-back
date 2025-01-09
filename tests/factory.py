from typing import Dict, Any

from tests.utility import make_random_string


def make_king_signup_data(
    overrides: Dict[str, Any] = None
) -> Dict[str, Any]:
    king_data = {
        "nick": make_random_string(),
        "email": f"{make_random_string()}@example.com",
        "password": "password",
    }
    if overrides:
        king_data.update(overrides)
    return king_data
