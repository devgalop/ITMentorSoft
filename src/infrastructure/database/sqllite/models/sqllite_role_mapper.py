from src.features.user_management.shared.role import Role
from src.infrastructure.database.sqllite.models.sqllite_role_model import RoleEntity


class SqlLiteRoleMapper:
    """A mapper class to convert between Role entities and Role domain models."""

    @staticmethod
    def to_model(role_entity: RoleEntity) -> Role:
        """Converts a RoleEntity to a Role domain model.

        Args:
            role_entity (RoleEntity): The RoleEntity to convert.

        Returns:
            Role: The corresponding Role domain model.
        """
        return Role(
            role_id=role_entity.id,
            name=role_entity.name,
            description=role_entity.description,
        )

    @staticmethod
    def to_entity(role: Role) -> RoleEntity:
        """Converts a Role domain model to a RoleEntity.


        Args:
            role (Role): The Role domain model to convert.

        Returns:
            RoleEntity: The corresponding RoleEntity.
        """
        return RoleEntity(id=role.role_id, name=role.name, description=role.description)
