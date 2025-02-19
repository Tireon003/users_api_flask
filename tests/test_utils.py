import pytest

from app.src.utils import validate_domain


class TestUtils:

    @pytest.mark.parametrize(
        ("domain", "expected_value"),
        (
            ("mail.ru", True),
            ("googlecom", False),
            ("ab.co.uk", True),
            ("example.a", False),
        ),
    )
    def test_validate_domain(
        self,
        domain: str,
        expected_value: bool,
    ) -> None:
        """Test for domain validation."""
        assert validate_domain(domain) == expected_value
