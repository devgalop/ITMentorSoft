from dotenv import load_dotenv
import os

from src.features.user_management.shared.password_hasher import PasswordHasher
from src.features.user_management.shared.token_generator import TokenGenerator
from src.features.user_management.shared.user_recovery_token_repository import RecoveryTokenInfo, UserRecoveryTokenRepository
from src.features.shared.notification_service import NotificationConfigBuilder, NotificationService
from src.features.user_management.recovery_password.recovery_password_request import RecoveryPasswordRequest
from src.features.user_management.recovery_password.recovery_password_response import RecoveryPasswordResponse
from src.features.user_management.shared.user_repository import UserRepository

load_dotenv()


MESSAGE_RECOVERY_TEMPLATE = "<p>Hello %USER%,</p><p>You requested a password recovery. Please click the link below to reset your password:</p><p><a href='%URL_BASE%?token=%URL_TOKEN%&trx=%ID_TRX%'>Reset Password</a></p><p>If you did not request this, please ignore this email.</p>"
EMAIL_RECOVERY_SUBJECT = "Recovery Password Instructions"
EMAIL_RECOVERY_SENDER = os.getenv("EMAIL_RECOVERY_SENDER", "")
RECOVERY_URL_BASE = os.getenv("RECOVERY_URL_BASE", "")

class RecoveryPasswordHandler:
    def __init__(self, 
                 user_repository: UserRepository,
                 user_recovery_token_repository: UserRecoveryTokenRepository, 
                 notification_service: NotificationService,
                 token_generator: TokenGenerator,
                 password_hasher: PasswordHasher):
        self.user_repository = user_repository
        self.user_recovery_token_repository = user_recovery_token_repository
        self.notification_service = notification_service
        self.token_generator = token_generator
        self.password_hasher = password_hasher

    async def handle(self, request: RecoveryPasswordRequest) -> RecoveryPasswordResponse:
        
        response_message = "If the email exists in our system, you will receive a password recovery email shortly."
        user = await self.user_repository.get_user_response_by_email(request.email)
        if not user:
            return RecoveryPasswordResponse(message=response_message)
        
        await self.user_recovery_token_repository.revoke_tokens_by_user_id(user.id)
        token = self.token_generator.generate_random_token()
        hashed_token = self.password_hasher.hash_password(token.token)
        recovery_token_info = RecoveryTokenInfo(
            user_id=user.id,
            token=hashed_token,
            expiration_time=token.expiration_time,
            status="active"
        )
        
        await self.user_recovery_token_repository.save_token(recovery_token_info)
        
        notification_config_builder = NotificationConfigBuilder(
                                        EMAIL_RECOVERY_SENDER,
                                        request.email,
                                        EMAIL_RECOVERY_SUBJECT)
        
        html_content = MESSAGE_RECOVERY_TEMPLATE.replace("%URL_BASE%", RECOVERY_URL_BASE).replace("%URL_TOKEN%", token.token).replace("%USER%", user.username).replace("%ID_TRX%", recovery_token_info.id_trx)
        
        notification_config_builder.set_template(html_content)
        notification_config = notification_config_builder.build()
        
        await self.notification_service.send_notification(notification_config)
        
        return RecoveryPasswordResponse(message=response_message)        