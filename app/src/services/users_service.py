from typing import TYPE_CHECKING

from app.src.models import User
from app.src.utils import validate_domain

if TYPE_CHECKING:
    from app.src.repositories import UserRepository


class UserService:
    """
    Service class for User model.
    """

    def __init__(self, repo: "UserRepository") -> None:
        self._repo = repo

    def count_registered_last_week(self) -> int:
        """
        Count registered users last week.
        :return: count of registered users
        """
        users_list = self._repo.get_all_filter_by_registered_date(days=7)
        return len(users_list)

    def get_top_5_longest_username(self) -> list[User]:
        """
        Get top 5 users with the longest username.
        :return: list of users
        """
        users_list = self._repo.get_order_by_longest_username(limit=5)
        return users_list

    def get_proportion_with_domain(self, domain: str) -> float:
        """
        Get proportion of users with the specified domain.
        :param domain: domain
        :return: proportion of users with the specified domain
        """
        if not validate_domain(domain):
            raise ValueError("Provided domain is not valid")

        count_all = self._repo.get_all_count()
        count_match_domain = self._repo.get_count_matching_email_domain(domain)

        proportion = round(count_match_domain / count_all, 2)

        return proportion
