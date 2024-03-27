from typing import Optional
from sqlmodel import Session, select, desc
from sqlmodel import Field, SQLModel, create_engine

from src.config import Config
from src.utils import get_current_time


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str
    content: str
    image: Optional[str] = None
    date: str


class Memory:
    def __init__(self):
        self.db_name = Config().get_sqlite_db()
        self.engine = create_engine(f"sqlite:///{self.db_name}")
        SQLModel.metadata.create_all(self.engine)

    def add_interaction(self, role, content, image=None, date=None):
        interaction = Conversation(role=role, content=content, image=image, date=date)
        with Session(self.engine) as session:
            session.add(interaction)
            session.commit()

    def get_interactions(self, limit=None):
        with Session(self.engine) as session:
            query = select(Conversation).order_by(desc(Conversation.id))
            if limit:
                query = query.limit(limit)
            interactions = session.exec(query).all()
            interactions_ascending = list(reversed(interactions))
            return interactions_ascending
