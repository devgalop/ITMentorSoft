from src.features.user_management.shared.user_recovery_token_repository import (
    RecoveryTokenInfo,
    UserRecoveryTokenResponse,
)
from src.infrastructure.database.sqllite.models.sqllite_user_recovery_token_model import (
    RecoveryTokenEntity,
)


class SqlLiteRecoveryTokenMapper:
    @staticmethod
    def to_model(
        recovery_token_entity: RecoveryTokenEntity,
    ) -> UserRecoveryTokenResponse:
        """Convert a RecoveryTokenEntity to a UserRecoveryTokenResponse.

        Args:
            recovery_token_entity (RecoveryTokenEntity): The entity to be converted.

        Returns:
            UserRecoveryTokenResponse: The resulting UserRecoveryTokenResponse.
        """
        return UserRecoveryTokenResponse(
            user_id=recovery_token_entity.user_id,
            token_hashed=recovery_token_entity.token,
            expiration_time=recovery_token_entity.expitation_time,
            status=recovery_token_entity.status,
        )

    @staticmethod
    def to_entity(recovery_token_info: RecoveryTokenInfo) -> RecoveryTokenEntity:
        """Convert a RecoveryTokenInfo to a RecoveryTokenEntity.

        Args:
            recovery_token_info (RecoveryTokenInfo): The information to be converted.

        Returns:
            RecoveryTokenEntity: The resulting RecoveryTokenEntity.
        """
        return RecoveryTokenEntity(
            id=recovery_token_info.id_trx,
            token=recovery_token_info.token,
            expitation_time=recovery_token_info.expiration_time,
            status=recovery_token_info.status,
            user_id=recovery_token_info.user_id,
        )
