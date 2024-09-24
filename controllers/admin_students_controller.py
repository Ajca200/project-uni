import os
import smtplib
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from PyQt5.QtWidgets import QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Local imports
from models._base import SessionLocal
from models._users import Student, Representante
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

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

    @classmethod    
    def get_data_student(cls, id):
        try:
            with SessionLocal() as session:
                resultado = session.query(Student, Representante).filter(and_(
                    Student.id_student == id,
                    Representante.id_representante == Student.fk_id_representante)).one_or_none()

                if resultado is None:
                    raise NoResultFound
                
                students_columns = [getattr(resultado[0], columna) for columna in resultado[0].__table__.columns.keys()]
                representante_columns = [getattr(resultado[1], columna) for columna in resultado[1].__table__.columns.keys()]

                return students_columns + representante_columns

        except NoResultFound:
            QMessageBox.warning(None, 'Error', 'No se han encontrado datos en la base de datos!')
            return []
        except SQLAlchemyError as e:
            print(e)
            QMessageBox.critical(None, 'Error', f"Ha ocurrido un error en la base de datos: {e}")
            return []
        except Exception as e:
            print(e)
            QMessageBox.critical(None, 'Error', f'Ha ocurrido un error inesperado: {e}')
            return []
        
    @classmethod
    def send_email(cls, message, email):
        """Envía un correo electrónico con el código de recuperación"""
        subject = 'Unidad Educativa Doctor Francisco Javier Garcia de Hevia'
        body = f"""
        <html>
        <body>
            <p>{message}</p>
        </body>
        </html>
        """

        msg = cls.create_email_message(SENDER_EMAIL, email, subject, body)

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, email, msg.as_string())
                print('Correo enviado exitosamente!')
                return True
        except Exception as e:
            cls.log_error(e)
            return False

    @staticmethod
    def create_email_message(sender_email, recipient_email, subject, body):
        """Crea un mensaje de correo electrónico"""
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, 'html'))
        return msg