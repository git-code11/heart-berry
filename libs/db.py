from typing import Optional, Any
from datetime import datetime

from sqlalchemy import create_engine, func

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.types import (
    String
)

from sqlalchemy.schema import (
    ForeignKey
)

import bson
import bcrypt
import argparse


type Record = dict[str, Any]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40))
    encrypted_password: Mapped[Optional[bytes]]
    records: Mapped[list["Analysis"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, \
        name={self.name!r}, \
        email={self.email!r})"

    @property
    def password(self): raise NotImplementedError()

    @password.setter
    def password(self, value: str):
        password = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        self.encrypted_password = password

    def check_password(self, value: str):
        return bcrypt.checkpw(value.encode(), self.encrypted_password)


class Analysis(Base):
    __tablename__ = "analysis"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    encoded_data: Mapped[Optional[bytes]]
    user: Mapped[User] = relationship(back_populates="records")
    created: Mapped[datetime] = mapped_column(
        server_default=func.current_date())
    # __data: Optional[Record]

    def __init__(self, **kwargs):
        data = kwargs.get('data', None)
        if data:
            self._data = data
            data = bson.dumps(data)
            kwargs['encoded_data'] = data
        else:
            self._data = None
        super().__init__(**kwargs)

    @property
    def data(self) -> Optional[Record]:
        _data = getattr(self, '_data', None)
        if _data and self.encoded_data is not None:
            self._data = bson.loads(self.encoded_data)
        return _data

    @data.setter
    def data(self, value: Optional[Record]):
        if value is not None:
            self._data = value
            # print("Value =>", value)
            self.encoded_data = bson.dumps(value)
        else:
            self._data = None
            self.encoded_data = None

    def __repr__(self) -> str:
        return f"Analysis(id={self.id!r}, user={self.user_id!r})"


def init_engine():
    engine = create_engine("sqlite:///data.db", echo=True)
    return engine


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="DB"
    )
    parser.add_argument('--init', action="store_true",
                        help="Intialise the database")
    param = parser.parse_args()

    if param.init:
        engine = init_engine()
        Base.metadata.create_all(engine)
