"""validate king state."""

from app.schema import KingPrivateData


def validate_king_slice(king_slice):
    """Validate the king slice of a state."""
    for id_str, king_data in king_slice.items():
        assert "id" in king_data
        assert id_str == str(king_data["id"])
        KingPrivateData.model_validate(king_data)
