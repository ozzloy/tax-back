"""utility functionality for schemas."""

from pydantic import BaseModel
from typing import Any, Iterator


class DictModel(BaseModel):
    """pydantic model that can be used as a dict."""

    def __getitem__(self, key: str) -> Any:
        """Allow dict-like access: model['field']."""
        return self.model_dump()[key]

    def __iter__(self) -> Iterator[str]:
        """Make iterable like a dict."""
        return iter(self.model_dump())

    def __len__(self) -> int:
        """Return number of fields."""
        return len(self.model_dump())

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator."""
        return key in self.model_dump()

    def keys(self):
        """Return dict_keys object."""
        return self.model_dump().keys()

    def values(self):
        """Return dict_values object."""
        return self.model_dump().values()

    def items(self):
        """Return dict_items object."""
        return self.model_dump().items()

    def get(self, key: str, default: Any = None) -> Any:
        """Dict-like get method with default value."""
        return self.model_dump().get(key, default)

    def __delitem__(self, key: str) -> None:
        """Support del statement: del model[key]."""
        delattr(self, key)

    def __setitem__(self, key, value):
        """Support set statement: model[key] = value."""
        setattr(self, key, value)
