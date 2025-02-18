import re


def validate_domain(domain: str) -> bool:
    """
    Validate domain.
    :param domain: domain
    :return: True if domain is valid, False otherwise
    """
    regex = r"[A-Za-z0-9-]+[.][A-Za-z.]{2,}"
    return bool(re.match(regex, domain))
