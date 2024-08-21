import os
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from PyQt5.QtWidgets import QMessageBox

# Local imports
from models._base import SessionLocal
from models._users import Student

class AdminStudentController:
    @classmethod
    def get_data_all(cls):
        try:
            with SessionLocal() as session:
                results = session.query(Student).all()
                if not results:
                    raise NoResultFound
                
                # Assuming you want to return a list of dictionaries
                # with column names as keys and corresponding values.
                return [{column.name: getattr(row, column.name) for column in row.__table__.columns} for row in results]

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