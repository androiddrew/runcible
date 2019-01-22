import pytest
from molten.errors import FieldValidationError
from runcible.validation import ExtStringValidator


def test_ext_string_validator_displays_pattern_error_msg():
    validator = ExtStringValidator()

    email_pattern = r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})"
    err_message = "Email provided fails verification"

    with pytest.raises(FieldValidationError) as err:
        validator.validate(
            field=str,
            value="notanemail",
            pattern=email_pattern,
            pattern_err_msg=err_message,
        )
        assert str(err) == err_message
