from src.features.user_management.shared.refresh_token_repository import (
    RefreshTokenData,
    RefreshTokenInfo,
)
from src.infrastructure.database.sqllite.models.sqllite_user_refresh_token_model import (
    RefreshTokenEntity,
)


class SqlLiteRefreshTokenMapper:
    @staticmethod
    def to_model(refresh_token_entity: RefreshTokenEntity) -> RefreshTokenData:
        """Convert a RefreshTokenEntity to a RefreshTokenData.

        Args:
            refresh_token_entity (RefreshTokenEntity): The entity to be converted.

        Returns:
            RefreshTokenData: The resulting RefreshTokenData.
        """
        return RefreshTokenData(
            user_id=refresh_token_entity.user_id,
            token_hashed=refresh_token_entity.token,
            expiration_time=refresh_token_entity.expiration_time,
            status=refresh_token_entity.status,
        )

    @staticmethod
    def to_entity(refresh_token_info: RefreshTokenInfo) -> RefreshTokenEntity:
        """Convert a RefreshTokenInfo to a RefreshTokenEntity.

        Args:
            refresh_token_info (RefreshTokenInfo): The information to be converted.

        Returns:
            RefreshTokenEntity: The resulting RefreshTokenEntity.
        """
        return RefreshTokenEntity(
            id=refresh_token_info.id_trx,
            token=refresh_token_info.token,
            expiration_time=refresh_token_info.expiration_time,
            status=refresh_token_info.status,
            user_id=refresh_token_info.user_id,
        )
