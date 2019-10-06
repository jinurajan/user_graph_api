from jsonschema import Draft4Validator, FormatChecker
from jsonschema.exceptions import ValidationError
from incoming import datatypes, PayloadValidator


class EStringIncomingType(datatypes.Types):
    '''
        Enhanced datatype for matching String
    '''
    MAX_STRING_LEN = 2 * 1024  # 2 KB

    _DEFAULT_ERROR = 'Invalid data. A proper string is expected.'

    def __init__(self, required=None, error=None, *args, **kwargs):
        super(EStringIncomingType, self).__init__(
            required, error, *args, **kwargs)
        self.max_len = kwargs.get('max_len', self.MAX_STRING_LEN)
        self.min_len = kwargs.get('min_len', None)
        if self.min_len is not None:
            self.error = "{} Minimum length required is {}.".format(
                self.error, self.min_len)
        if self.max_len is not None:
            self.error = "{} Maximum length allowed is {}.".format(
                self.error, self.max_len)

    def validate(self, val, *args, **kwargs):
        if not isinstance(val, str):
            return False

        if (self.max_len is not None):
            if len(val) > self.max_len:
                return False

        if (self.min_len is not None):
            if len(val) < self.min_len:
                return False

        return True


class EEmailIncomingType(datatypes.Types):
    '''
        Enhanced datatype for matching Email
    '''

    _DEFAULT_ERROR = 'Invalid Email. A proper Email ID is expected.'

    def __init__(self, required=None, error=None, *args, **kwargs):
        super(EEmailIncomingType, self).__init__(
            required, error, *args, **kwargs)
        self.validator = Draft4Validator(
            {'type': 'string', 'format': 'email'},
            format_checker=FormatChecker())

    def validate(self, val, payload, errors, **kwargs):
        try:
            self.validator.validate(val)
            return True
        except ValidationError as e:
            errors.append(e.message)
            return False


class UserUpdationValidator(PayloadValidator):
    name = EStringIncomingType(
        required=True,
        min_len=1)
    phone = EStringIncomingType(
        required=True,
        max_len=25,
        min_len=6)
    strict = True


class UserCreationValidator(UserUpdationValidator):
    email = EEmailIncomingType(required=True)
    strict = True


class UserFollowCreationValidator(PayloadValidator):
    following_user_email = EStringIncomingType(
        required=True,
        min_len=6)
    strict = True
