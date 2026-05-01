from abc import ABC, abstractmethod

from src.features.user_management.shared.role import Role


class RoleRepository(ABC):
    """Interface for role repository implementations.

    Args:
        ABC (ABC): Abstract base class for role repository implementations.
    """

    @abstractmethod
    async def get_available_roles(self) -> list[Role]:
        """Get a list of available roles.

        Returns:
            list[Role]: A list of available role objects.
        """
        pass

    @abstractmethod
    async def get_role_by_id(self, role_id: str) -> Role | None:
        """Get a role by its ID.

        Args:
            role_id (str): The ID of the role to retrieve.

        Returns:
            Role: The role object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_role_by_name(self, name: str) -> Role | None:
        """Get a role by its name.

        Args:
            name (str): The name of the role to retrieve.

        Returns:
            Role: The role object if found, otherwise None.
        """
        pass
