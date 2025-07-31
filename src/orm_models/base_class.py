from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative, class_mapper

metadata = MetaData()


@as_declarative()
class Base:
    id: Any
    __name__: str
    metadata = metadata

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    def asdict(self):
        return {
            c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns
        }
