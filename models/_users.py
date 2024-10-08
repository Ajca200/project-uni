from sqlalchemy import Column, String, Date, INT
from models._base import Base

class User(Base):
    __tablename__ = 'tb_users'

    id_user = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(50), nullable=False)
    profile_picture = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<User(id='{self.id_user}', name='{self.name} {self.surname}')"
    
class Student(Base):
    __tablename__ = "tb_students"

    id_student = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    fk_id_representante = Column(String(50), nullable=False)
    fk_id_section = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Student(id='{self.id_student}', name='{self.name}')>"
    
class Representante(Base):
    __tablename__ = "tb_representante"

    id_representante = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    position = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Representante(id='{self.id_representante}', name='{self.name}')>"
    #................................................................
    
class Teachers (Base):
    __tablename__ = "tb_teachers"
    
    id_teacher = Column( String (50), primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    emil = Column (String (50), nullable = False)
    phone = Column ( INT, nullable= False )
    
    def __repr__(self):
        return f"<Teachers(id='{self.id_teacher}', name='{self.name}')>"
    
    
