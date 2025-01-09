from email_validator import validate_email, EmailNotValidError
from flask import current_app

from app.model.king import King


def validate_king_create_data(data):
    required_fields = ["nick", "email", "password"]
    errors = {
        field: f"{field} is required"
        for field in required_fields
        if field not in data
    }
    if errors:
        return {"message": "field missing", "errors": errors}, 400

    allowed_fields = required_fields
    errors = {
        field: f"{field} is forbidden"
        for field in data
        if field not in allowed_fields
    }
    if errors:
        return {"message": "extra field", "errors": errors}, 400

    errors = {
        key: f"{key} must have at least 1 character"
        for key, value in data.items()
        if not value
    }
    try:
        check_deliverability = current_app.config.get(
            "CHECK_EMAIL_DELIVERABILITY", True
        )
        validate_email(
            data["email"], check_deliverability=check_deliverability
        )
    except EmailNotValidError:
        errors["email"] = "invalid email"
    if errors:
        return {"message": "bad request", "errors": errors}, 422

    conflict_keys = ["nick", "email"]
    errors = {
        key: f"{key} is taken"
        for key in conflict_keys
        if King.query.filter_by(**{key: data[key]}).first()
    }
    if errors:
        return {"message": "account conflict", "errors": errors}, 409

    return None


def validate_king_data(king_data):
    assert isinstance(king_data["nick"], str)
    assert isinstance(king_data["email"], str)
    theme_id = king_data.get("theme_id")
    assert theme_id == None or isinstance(theme_id, int)


def validate_king_slice(king_slice):
    for id_str, king_data in king_slice.items():
        assert "id" in king_data
        assert id_str == str(king_data["id"])
        validate_king_data(king_data)
