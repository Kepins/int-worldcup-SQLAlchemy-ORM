from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    in_first_team: Mapped[List["Match"]] = relationship(back_populates="first_team", cascade="all, delete-orphan")
    in_second_team: Mapped[List["Match"]] = relationship(back_populates="second_team", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, name={self.name!r})"


class Match(Base):
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    second_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    first_team_score: Mapped[int]
    second_team_score: Mapped[int]

    first_team: Mapped["Team"] = relationship(back_populates="in_first_team", foreign_keys=[first_team_id])
    second_team: Mapped["Team"] = relationship(back_populates="in_second_team", foreign_keys=[second_team_id])

    def __repr__(self) -> str:
        return f"Match(id={self.id!r}, first_team={self.first_team!r}), second_team={self.second_team!r}, " \
               f"first_team_score={self.first_team_score!r}, second_team_score={self.second_team_score!r}"
