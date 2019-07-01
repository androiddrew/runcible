import re
from typing import Optional, Sequence
from molten.validation.field import StringValidator, Field, _T
from molten.errors import FieldValidationError


class ExtStringValidator(StringValidator):
    """Validates strings with extension for better error reporting."""

    def validate(
        self,
        field: Field[_T],
        value: str,
        choices: Optional[Sequence[str]] = None,
        pattern: Optional[str] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        strip_spaces: bool = False,
        pattern_err_msg: Optional[str] = None,
    ) -> str:
        if choices is not None and value not in choices:
            raise FieldValidationError(
                f"must be one of: {', '.join(repr(choice) for choice in choices)}"
            )

        if pattern is not None and not re.match(pattern, value):
            if pattern_err_msg is not None:
                raise FieldValidationError(f"{pattern_err_msg}")
            raise FieldValidationError(f"must match pattern {pattern!r}")

        if min_length is not None and len(value) < min_length:
            raise FieldValidationError(f"length must be >= {min_length}")

        if max_length is not None and len(value) > max_length:
            raise FieldValidationError(f"length must be <= {max_length}")

        if strip_spaces:
            return value.strip()

        return value
