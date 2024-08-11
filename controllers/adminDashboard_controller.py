from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

# Local imports
from models._base import SessionLocal
from models._users import User

class AdminDashboardController:
    @classmethod
    def get_data(cls, id):
        try:
            with SessionLocal() as session:
                result = session.query(User).filter(User.id_user == id).one()
                
                # Obtener los valores de los campos definidos en la tabla
                admin = [getattr(result, column.name) for column in result.__table__.columns]
                
                return admin
        except NoResultFound:
            print('No se ha encontrado ningún usuario con ese ID.')
            return False
        except SQLAlchemyError as e:
            print(f'Error en la base de datos: {e}')
            return False
        except Exception as e:
            print(f'Error inesperado: {e}')
            return False
