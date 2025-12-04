API_RESPONSE_ACTION_CODES = {"display_error_1": "DISPLAY_ERROR_MESSAGES"}

_COMMON_MESSAGES = {
    "null_blank": "This field cannot be empty. Please provide a value.",
    "invalid": "The provided value is invalid. Please check your input.",
}

CUSTOM_ERRORS_MESSAGES = {
    "Others": {
        "blank": _COMMON_MESSAGES["null_blank"],
        "null": _COMMON_MESSAGES["null_blank"],
        "invalid_choice": "The selected choice is invalid. Please select a valid option.",
    },
    "ManyRelatedField": {
        "empty": "Please select at least one option.",
    },
    "PrimaryKeyRelatedField": {
        "does_not_exist": (
            "The selected value does not exist. Please choose a valid option from the available choices."
        ),
        "incorrect_type": (
            "Invalid data type. Ensure your input matches the expected format."
        ),
    },
}
