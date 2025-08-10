from .repository import EntryRepository
from config.database import get_db_connection

from fastapi import Depends


def get_entry_repository(db = Depends(get_db_connection)):
    return EntryRepository(db)