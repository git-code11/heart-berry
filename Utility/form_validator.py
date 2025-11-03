import typing as tp
import re
from collections.abc import Iterable


type ValidationResult = tp.Optional[str]


class FormValidator:

    @classmethod
    def validate(cls, data: tp.Any) -> dict[str, str]:
        errors = dict()
        # extract type hints
        type_hints = tp.get_type_hints(data, include_extras=True)
        for (key, hint) in type_hints.items():
            value = getattr(data, key)
            if tp.get_origin(hint) is tp.Annotated:
                args = tp.get_args(hint)
                for arg in args:
                    arg = arg if isinstance(arg, Iterable) and type(
                        arg) is not str else (arg, )
                    if output := cls._validate(value, *arg):
                        errors[key] = output
                        break
            else:
                if output := cls._validate(value, *arg):
                    errors[key] = output
        return errors

    @classmethod
    def _validate(cls, value: tp.Any, hint: tp.Any,
                  *args, **kwargs) -> ValidationResult:
        hint_type = type(hint)
        if hint_type is type:
            return cls.check_type(value, hint, *args, *kwargs)
        func = getattr(cls, hint)
        return func(value, *args, *kwargs)

    @staticmethod
    def check_type(value: tp.Any, type_: tp.Any) -> ValidationResult:
        return None if type_ is type(value) else "Invalid data"

    @staticmethod
    def not_empty(value: str) -> ValidationResult:
        return "Value is empty" if value == "" else None

    @staticmethod
    def max_length(value: str, max_len: int) -> ValidationResult:
        return None if len(value) <= max_len else "Value is too large"

    @staticmethod
    def min_length(value: str, min_len: int) -> ValidationResult:
        return None if len(value) >= min_len else "Value is too small"

    @staticmethod
    def email(value: str) -> ValidationResult:
        if re.match(r'^.+[@].+$', value) is None:
            return "Invalid email"
        return None
