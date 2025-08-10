from fastapi import APIRouter, Depends
from typing import List

from .schemas import EntryCreate, Entry, EntryUpdate
from .di import get_entry_repository
from .repository import EntryRepository


router = APIRouter(
    prefix='/diary',
    tags=['Diary']
)


@router.post('/')
async def  create_diary(
    entry: EntryCreate, 
    entry_repository: EntryRepository = Depends(get_entry_repository)
) -> Entry:
    entry = await entry_repository.create_entry(entry)
    return entry


@router.get('/{id_entry}')
async def get_entry(
    id_entry: int,
    entry_repository: EntryRepository = Depends(get_entry_repository)
) -> Entry:
    entry = await entry_repository.get_entry_by_id(id_entry)
    return entry

@router.get('/')
async def get_list_entries(
    entry_repository: EntryRepository = Depends(get_entry_repository)
) -> List[Entry]:
    return await entry_repository.get_all_entries()

@router.put('/{id_entry}')
async def update_entry(
    id_entry: int,
    entry: EntryUpdate,
    entry_repository: EntryRepository = Depends(get_entry_repository)
) -> Entry:
    return await entry_repository.update_entry(id_entry, entry)

@router.patch('/{id_entry}')
async def mark_done(
    id_entry: int,
    entry_repository: EntryRepository = Depends(get_entry_repository)
) -> Entry:
    return await entry_repository.mark_entry_done(id_entry)


@router.delete('/{id_entry}')
async def delete_entry(
    id_entry: int,
    entry_repository: EntryRepository = Depends(get_entry_repository)
):
    await entry_repository.delete_entry(id_entry)