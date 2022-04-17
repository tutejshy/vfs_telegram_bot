from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class BaseDB:
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
