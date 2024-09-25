import os
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from PyQt5.QtWidgets import QMessageBox

# Local imports
from models._base import SessionLocal 
from models._users import Teachers

class AdminTeachercontroller:
     @classmethod
     def get__data__all(clas):
         try:
            with SessionLocal() as session:
             results= session.query(Teachers).all()
             if results:
                return [{column.name: getattr(row, column.name) for column in row.__table__.columns} for row in results]
             raise NoResultFound
         
         except NoResultFound:
              QMessageBox.warning(None, 'Error', 'No se han encontrado resultados!')
              return []
         except SQLAlchemyError as e:
            print(e)
            QMessageBox.critical(None, 'Error', f"Ha ocurrido un error en la base de datos: {e}")
            return []
         except Exception as e:
            print(e)
            QMessageBox.critical(None, 'Error', f'Ha ocurrido un error inesperado: {e}')
            return []
