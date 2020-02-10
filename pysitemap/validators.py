import re


class ValidationFailure(BaseException):
    """
    class for Validation exceptions
    """


domain_pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)


def domain(value, raise_errors=True):
    """
    Return whether or not given value is a valid domain.

    If the value is valid domain name this function returns ``True``, otherwise
    :class:`~validators.ValidationFailure` or False if raise_errors muted.

    Examples::
        >>> domain('example.com')
        True

        >>> domain('example.com/')
        ValidationFailure(func=domain, ...)

    Supports IDN domains as well::

        >>> domain('xn----gtbspbbmkef.xn--p1ai')
        True
    :param value: domain string to validate
    :param raise_errors: raise errors or return False
    """
    if domain_pattern.match(value) is None:
        if raise_errors:
            raise ValidationFailure("{} is not valid domain".format(value))
        else:
            return False
    return True

