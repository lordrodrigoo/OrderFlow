from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.account import Account

class AccountRepositoryInterface(ABC):
    """This interface defines the contract for account repository."""

    @abstractmethod
    def create_account(self, account: Account) -> Account: pass

    @abstractmethod
    def update_account(self, account: Account) -> Account: pass

    @abstractmethod
    def find_all_accounts(self) -> List[Account]: pass

    @abstractmethod
    def find_account_by_id(self, account_id: int) -> Optional[Account]: pass

    @abstractmethod
    def delete_account(self, account_id: int) -> bool: pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[Account]: pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Account]: pass


    @abstractmethod
    def update_password(self, account_id: int, new_password_hash: str) -> Optional[Account]: pass

    @abstractmethod
    def update_status(self, account_id: int, new_status: str) -> Optional[Account]: pass
