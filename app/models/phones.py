from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Phone(Base):
    phone_number: Mapped[int] = mapped_column(unique=True)
    display_name: Mapped[str] = mapped_column(unique=False)
    last_ip: Mapped[str] = mapped_column(unique=False, nullable=True)
