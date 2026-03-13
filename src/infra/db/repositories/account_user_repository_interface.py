from typing import List, Optional
from datetime import datetime
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.account import AccountEntity
from src.domain.repositories.account_repository import AccountRepositoryInterface
from src.domain.models.account import Account, AccountStatus
from src.infra.db.repositories.base_repository import BaseRepository


class AccountRepository(AccountRepositoryInterface, BaseRepository[AccountEntity]):
    def __init__(self, db_connection: DBConnectionHandler):
        super().__init__(db_connection.session, AccountEntity)

    def create_account(self, account: Account) -> Account:
        now = datetime.now()
        entity = AccountEntity(
            id=account.id,
            user_id=account.user_id,
            username=account.username,
            password_hash=account.password_hash,
            status=account.status.value,  #Save as string
            created_at=now,
            updated_at=now
        )
        self.add(entity)
        self.save()

        return Account.from_entity(entity)

    def update_account(self, account: Account) -> Optional[Account]:
        if account.id is None:
            raise ValueError("Account ID must be provided for update.")
        entity = self.get_by_id(account.id)
        if not entity:
            return None

        entity.user_id = account.user_id
        entity.username = account.username
        entity.password_hash = account.password_hash
        entity.status = account.status.value
        entity.updated_at = datetime.now()
        self.save()

        return Account.from_entity(entity)

    def find_all_accounts(self) -> List[Account]:
        return [Account.from_entity(entity) for entity in self.get_all()]

    def find_account_by_id(self, account_id: int) -> Optional[Account]:
        entity = self.get_by_id(account_id)
        return Account.from_entity(entity) if entity else None


    def find_by_username(self, username: str) -> Optional[Account]:
        entity = self.session.query(AccountEntity).filter_by(username=username).first()
        return Account.from_entity(entity) if entity else None

    def delete_account(self, account_id: int) -> bool:
        return self.delete_by_id(account_id)


    def find_by_user_id(self, user_id: int) -> Optional[Account]:
        entity = self.session.query(AccountEntity).filter_by(user_id=user_id).first()
        return Account.from_entity(entity) if entity else None


    def update_password(self, account_id: int, new_password_hash: str) -> Optional[Account]:
        entity = self.get_by_id(account_id)
        if not entity:
            return None

        entity.password_hash = new_password_hash
        entity.updated_at = datetime.now()
        self.save()
        return Account.from_entity(entity)

    def update_status(self, account_id: int, new_status: AccountStatus) -> Optional[Account]:
        entity = self.get_by_id(account_id)
        if not entity:
            return None

        entity.status = new_status.value
        entity.updated_at = datetime.now()
        self.save()
        return Account.from_entity(entity)
