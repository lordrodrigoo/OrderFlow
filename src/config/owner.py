import os
import logging
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.repositories.user_repository_interface import UserRepository
from src.infra.db.repositories.account_user_repository_interface import AccountRepository
from src.domain.models.user import Users, UserRole
from src.domain.models.account import Account, AccountStatus
from src.config.security import hash_password

logger = logging.getLogger(__name__)

_REQUIRED_VARS = ("OWNER_EMAIL", "OWNER_USERNAME", "OWNER_PASSWORD")


def seed_owner() -> None:
    """
    Creates the system owner on first startup if one does not exist yet.
    Requires OWNER_EMAIL, OWNER_USERNAME and OWNER_PASSWORD env vars.
    Skipped silently when those vars are absent (e.g. during tests).
    """
    missing = [v for v in _REQUIRED_VARS if not os.getenv(v)]
    if missing:
        logger.info("Owner seeder skipped — missing env vars: %s", missing)
        return

    owner_email = os.getenv("OWNER_EMAIL")
    owner_username = os.getenv("OWNER_USERNAME")
    owner_password = os.getenv("OWNER_PASSWORD")
    owner_first_name = os.getenv("OWNER_FIRST_NAME", "System")
    owner_last_name = os.getenv("OWNER_LAST_NAME", "Owner")

    with DBConnectionHandler() as db:
        user_repo = UserRepository(db)
        account_repo = AccountRepository(db)

        existing_owners = user_repo.get_user_by_role(UserRole.OWNER)
        if existing_owners:
            logger.info("Owner already exists — seeder skipped")
            return

        if user_repo.find_by_email(owner_email):
            logger.warning(
                "Owner seeder: email '%s' already registered as a different role — skipped",
                owner_email,
            )
            return

        if account_repo.find_by_username(owner_username):
            logger.warning(
                "Owner seeder: username '%s' already taken — skipped",
                owner_username,
            )
            return

        user = Users(
            first_name=owner_first_name,
            last_name=owner_last_name,
            age=18,
            phone="00000000000",
            email=owner_email,
            is_active=True,
            role=UserRole.OWNER,
        )
        created_user = user_repo.create_user(user)

        account = Account(
            user_id=created_user.id,
            username=owner_username,
            password_hash=hash_password(owner_password),
            status=AccountStatus.ACTIVE,
        )
        account_repo.create_account(account)

        logger.info("System owner created successfully")
