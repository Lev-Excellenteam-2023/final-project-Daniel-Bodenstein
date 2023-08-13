import uuid
import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, create_engine, Uuid
from sqlalchemy import String, Enum
from sqlalchemy.orm import DeclarativeBase, validates, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from email_validate import validate

engine = create_engine("sqlite:///C://Users//User//Desktop//exelenteam//project//EndOfCourseProject//final-project-Daniel-Bodenstein//SQL.db", echo=True)

_session = sessionmaker(bind=engine)


class Status(enum.Enum):
    PENDING = 1
    COMPLETE = 2
    SENT = 3


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String)

    uploads: Mapped[List["Upload"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "uploads": [upload.to_dict() for upload in self.uploads]
        }

    @validates('email')
    def validate_email(self, key, email):
        if not validate(email_address=email, check_format=True, check_smtp=False):
            raise ValueError('Invalid email format')
        if not validate(email_address=email, check_smtp=True):
            raise ValueError('Email does not exist')
        return email

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Upload(Base):
    __tablename__ = "upload"

    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[uuid] = mapped_column(Uuid, default=uuid.uuid4())
    filename: Mapped[str] = mapped_column(String)
    upload_time: Mapped[datetime]
    finish_time: Mapped[Optional[datetime]]
    status = mapped_column(Enum(Status), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))

    user: Mapped[Optional["User"]] = relationship(back_populates="uploads")

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "filename": self.filename,
            "upload_time": self.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
            "finish_time": self.finish_time.strftime("%Y-%m-%d %H:%M:%S") if self.finish_time else None,
            "status": self.status.name,
            "user_id": self.user_id
        }

    @property
    def upload_path(self):
        return 'uploads\\' + str(self.uid)

    @property
    def download_path(self):
        return 'downloads\\' + str(self.uid)

    def __repr__(self) -> str:
        return f"Upload(id={self.id!r}, uid={self.uid!r}, user_id={self.user_id}, status={self.status})"


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
