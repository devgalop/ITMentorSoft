from src.features.user_management.assign_role.assign_role_request import (
    AssignRoleRequest,
)
from src.features.user_management.assign_role.assign_role_response import (
    AssignRoleResponse,
)
from src.features.user_management.shared.user_repository import UserRepository


class AssignRoleHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, request: AssignRoleRequest) -> AssignRoleResponse:
        """Handle the role assignment request.

        Args:
            request (AssignRoleRequest): The request object containing user ID and role information.

        Returns:
            AssignRoleResponse: The response object containing the result of the role assignment.
        """
        try:
            available_roles = await self.user_repository.get_available_roles()
            if request.role not in available_roles:
                return AssignRoleResponse(
                    is_success=False, message="Invalid role specified."
                )
            await self.user_repository.assign_role_to_user(request)
            return AssignRoleResponse(
                is_success=True, message="Role assigned successfully."
            )
        except Exception as e:
            return AssignRoleResponse(is_success=False, message=str(e))
