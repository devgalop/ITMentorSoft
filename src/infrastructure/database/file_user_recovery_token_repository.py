import aiofiles
from pathlib import Path
from src.features.user_management.shared.user_recovery_token_repository import (
    RecoveryTokenInfo,
    UserRecoveryTokenRepository,
    UserRecoveryTokenResponse,
)


class FileUserRecoveryTokenRepository(UserRecoveryTokenRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        file_db = Path(file_path)
        file_db.touch(exist_ok=True)

    async def save_token(self, recovery_token_info: RecoveryTokenInfo):
        """Save the generated token along with the associated user ID and expiration time.

        Args:
            recovery_token_info (RecoveryTokenInfo): The information about the recovery token.
        """
        async with aiofiles.open(self.file_path, "a") as f:
            await f.write(
                f"{recovery_token_info.user_id},{recovery_token_info.token},{recovery_token_info.expiration_time},{recovery_token_info.status},{recovery_token_info.id_trx}\n"
            )

    async def get_user_id_by_transaction_id(
        self, transaction_id: str
    ) -> UserRecoveryTokenResponse | None:
        """Retrieve the user recovery token response associated with a given transaction ID.

        Args:
            transaction_id (str): The transaction ID to search for.

        Returns:
            UserRecoveryTokenResponse: The user recovery token response associated with the transaction ID if found, otherwise None.
        """
        async with aiofiles.open(self.file_path, "r") as f:
            async for line in f:
                data = line.strip().split(",")
                if data[3] == "active" and data[4] == transaction_id:
                    return UserRecoveryTokenResponse(
                        user_id=data[0],
                        token_hashed=data[1],
                        expiration_time=float(data[2]),
                        status=data[3],
                    )
        return None

    async def revoke_token(self, token: str):
        """Revoke a recovery token from the repository.

        Args:
            token (str): The recovery token to be revoked.
        """
        async with aiofiles.open(self.file_path, "r") as f:
            lines = await f.readlines()
        async with aiofiles.open(self.file_path, "w") as f:
            for line in lines:
                data = line.strip().split(",")
                if data[1] == token:
                    data[3] = "revoked"
                await f.write(",".join(data) + "\n")

    async def revoke_tokens_by_user_id(self, user_id: str):
        """Revoke all recovery tokens associated with a given user ID.

        Args:
            user_id (str): The ID of the user whose tokens should be revoked.
        """
        async with aiofiles.open(self.file_path, "r") as f:
            lines = await f.readlines()
        async with aiofiles.open(self.file_path, "w") as f:
            for line in lines:
                data = line.strip().split(",")
                if data[0] == user_id:
                    data[3] = "revoked"
                await f.write(",".join(data) + "\n")
