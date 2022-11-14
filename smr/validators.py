import string
from django.core.exceptions import ValidationError

def contains_special_character(value):
    for char in value:
        if char in string.punctuation:
            return True
    return False

def contains_uppercase_letter(value):
    return True

def contains_lowercase_letter(value):
    return True

def contains_number(value):
    return True


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if(
            len(password)<8 or
            not contains_uppercase_letter(password) or
            not contains_lowercase_letter(password) or
            not contains_number(password) or
            not contains_special_character(password)
        ):
            raise ValidationError("비밀번호는 8자 이상의 영문 대/소문자, 숫자, 특수 문자를 조합해야 합니다.")
    
    def get_help_text(self):
        return "비밀번호는 8자 이상의 영문 대/소문자, 숫자, 특수 문자를 조합해야 합니다."

def validate_no_special_characters(value):
    if contains_special_character(value):
        raise ValidationError("특수 문자를 포함할 수 없습니다.")


def weight_validator(value):
    if value < 0:
        raise ValidationError("0보다 낮은 무게는 사용할 수 없습니다.")

def percentage(value):
    if value < 0 or value > 100:
        raise ValidationError("체지방률은 백분율 값입니다.")