from sqlalchemy import Column, String, DateTime, Integer
from models._base import Base
import datetime

class Email(Base):
    __tablename__ = 'tb_email_blocking'

    id_lock = Column(String(50), primary_key=True, nullable=False)
    id_user_lock = Column(String(50), nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
    blocking_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return f'<Blocked email("{self.id_user_lock}")>'

    def reset_attempts_if_needed(self):
        if self.blocking_time:
            elapsed_time = datetime.datetime.now() - self.blocking_time
            if elapsed_time > datetime.timedelta(hours=24):
                self.attempts = 0
                self.blocking_time = None

    def increment_attempts(self):
        self.attempts += 1
        if self.attempts >= 3:
            self.blocking_time = datetime.datetime.now()

    def is_blocked(self):
        if self.attempts >= 3:
            elapsed_time = datetime.datetime.now() - self.blocking_time
            if elapsed_time < datetime.timedelta(hours=24):
                return True
        return False
