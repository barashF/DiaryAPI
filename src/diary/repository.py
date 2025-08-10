from asyncpg import Connection
from fastapi import HTTPException, status
from typing import List

from .schemas import EntryCreate, EntryBase, EntryUpdate, Entry


class EntryRepository:
    def __init__(self, db_context: Connection):
        self.db_context = db_context
    

    async def create_entry(self, entry: EntryCreate) -> Entry:
        query = """
            INSERT INTO entries (title, content)
            VALUES ($1, $2)
            RETURNING id, title, content, is_done, created_at
        """
        row = await self.db_context.fetchrow(
            query,
            entry.title,
            entry.content
        )
        return Entry(**row)
    
    async def get_entry_by_id(self, id_entry: int) -> Entry:
        query = """
            SELECT id, title, content, is_done, created_at
            FROM entries
            WHERE id = $1
        """

        row = await self.db_context.fetchrow(
            query,
            id_entry
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Entry not found'
            )
        return Entry(**row)
    
    async def get_all_entries(self) -> List[Entry]:
        query = """
            SELECT id, title, content, is_done, created_at
            FROM entries
        """
        rows = await self.db_context.fetch(query)
        return [Entry(**row) for row in rows]

    async def update_entry(self, id_entry: int, entry: EntryUpdate) -> Entry:
        await self.get_entry_by_id(id_entry)
        update_data = entry.model_dump(exclude_unset=True)
      
        if not update_data:
            return await self.get_entry_by_id(entry_id)
        
        set_clause = ", ".join([f"{field} = ${i+1}" for i, field in enumerate(update_data.keys())])
        query = f"""
            UPDATE entries
            SET {set_clause}
            WHERE id = ${len(update_data) + 1}
            RETURNING id, title, content, is_done, created_at
        """
        
        params = list(update_data.values()) + [id_entry]
        updated_entry = await self.db_context.fetchrow(query, *params)
        return Entry(**updated_entry)
    
    async def mark_entry_done(self, id_entry) -> Entry:
        await self.get_entry_by_id(id_entry)

        query = """
            UPDATE entries
            SET is_done = True
            WHERE id = $1
            RETURNING id, title, content, is_done, created_at
        """
        row = await self.db_context.fetchrow(
            query,
            id_entry
        )
        return Entry(**row)

    async def delete_entry(self, id_entry: int):
        await self.get_entry_by_id(id_entry)
        query = """DELETE FROM entries WHERE id = $1"""
        await self.db_context.fetchrow(query, id_entry)
