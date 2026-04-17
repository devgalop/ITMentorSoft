from src.features.user_management.get_available_roles.get_available_roles_response import (
    GetAvailableRolesResponse,
)
from src.features.user_management.shared.user_repository import UserRepository


class GetAvailableRolesHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self) -> GetAvailableRolesResponse:
        """Handle the request to get available roles.

        Returns:
            GetAvailableRolesResponse: A response object containing the list of available roles.
        """
        try:
            roles = await self.user_repository.get_available_roles()
            return GetAvailableRolesResponse(is_success=True, roles=roles)
        except Exception:
            return GetAvailableRolesResponse(is_success=False, roles=[])
