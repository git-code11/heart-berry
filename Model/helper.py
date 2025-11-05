from typing import Optional
from libs.db import User, Analysis
from sqlalchemy.sql import expression as E
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class DBHelper:

    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_session(self, *args, **kwargs) -> Session:
        return Session(self.engine, *args, **kwargs)

    def create_user(self, name: str, email: str, password: str) -> User:
        user = User(name=name, email=email.lower())
        user.password = password
        with self.get_session(expire_on_commit=False) as session:
            session.add(user)
            session.commit()
        return user

    def reset_password(self, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if user:
            user.password = password
            with self.get_session(expire_on_commit=False) as session:
                session.add(user)
                session.commit()
        return user

    def get_user_by_id(self, id: int):
        with self.get_session() as session:
            user = session.get(User, id)
            return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        with self.get_session() as session:
            stmt = E.select(User).where(User.email == email.lower())
            user = session.scalar(stmt)
            return user

    def has_user(self, email: str) -> bool:
        with self.get_session() as session:
            stmt = E.select(E.true()).where(User.email == email.lower())
            return session.scalar(stmt)

    def create_record(self, user_id: int, data: dict) -> Analysis:
        record = Analysis(user_id=user_id)
        record.data = data
        with self.get_session(expire_on_commit=False) as session:
            session.add(record)
            session.commit()
        return record

    def get_records(self, user_id: int) -> list[Analysis]:
        with self.get_session() as session:
            stmt = E.select(Analysis) \
                .where(Analysis.user_id ==
                       user_id).order_by(Analysis.created.desc())
            records = session.scalars(stmt)
            return records.all()
