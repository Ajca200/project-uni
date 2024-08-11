from sqlalchemy import Column, Integer, String, Text
from models._base import Base

class Credentials(Base):
    __tablename__ = 'tb_credenciales'

    id_credencial = Column(Integer, primary_key=True, index=True)
    id_username = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)
    position = Column(String(50), nullable=False)
    fk_user_id = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Credential(username='{self.id_username}', rol='{self.position}')>"
