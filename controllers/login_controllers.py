import os
import smtplib
import pytz
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash

# Local imports
from models._base import SessionLocal
from models._credentials import Credentials
from models._users import User
from models._locks import Email

# Constantes para mensajes
MSG_SUCCESS = 'Bienvenido!'
MSG_INVALID_CREDENTIALS = 'Usuario o contraseña incorrecto \n compruebe e intente nuevamente'
MSG_UNEXPECTED_ERROR = 'Ha ocurrido un error inesperado: {}'
MSG_INVALID_EMAIL = 'Este usuario o correo electrónico no se encuentra registrado \n compruebe e intente nuevamente.'

# Configuración del servidor SMTP y credenciales
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "colmenaresabrahan5f@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "aotv kqyk teyv gxyg")

# date
UTC = pytz.timezone("America/Caracas")

class LoginController:
    @classmethod
    def authenticate(cls, username, password):
        """ Autentica el usuario y la contraseña en la base de datos """
        if not username or not password:
            return False, 'warning', 'Por favor ingrese usuario y contraseña.'

        try:
            with SessionLocal() as session:
                results = session.query(Credentials).filter(Credentials.id_username == username).one()
                if check_password_hash(results.password, password):
                    return results.fk_user_id, results.position, MSG_SUCCESS
                else:
                    return False, 'warning', MSG_INVALID_CREDENTIALS
        except NoResultFound:
            return False, 'warning', MSG_INVALID_CREDENTIALS
        except SQLAlchemyError as e:
            cls.log_error(e)
            return False, 'critical', MSG_UNEXPECTED_ERROR.format(e)
        except Exception as e:
            cls.log_error(e)
            return False, 'critical', MSG_UNEXPECTED_ERROR.format(e)

    @classmethod
    def forgot_password(cls, id, email):
        """ Verifica si el correo electrónico existe en la base de datos """
        if not email:
            return False, 'warning', 'Por favor ingrese un correo electrónico.'

        try:
            with SessionLocal() as session:
                results = session.query(User).filter(and_(
                    User.id_user == id,
                    User.email == email)).one()

                return True, results.email, MSG_SUCCESS
        except NoResultFound:
            return False, 'warning', MSG_INVALID_EMAIL
        except SQLAlchemyError as e:
            cls.log_error(e)
            return False, 'critical', MSG_UNEXPECTED_ERROR.format(e)
        except Exception as e:
            cls.log_error(e)
            return False, 'critical', MSG_UNEXPECTED_ERROR.format(e)

    @classmethod
    def send_email(cls, code, email):
        """ Envía un correo electrónico con el código de recuperación """
        recipient_email = email
        subject = 'Recuperación de contraseña'
        body = f"""
        <html>
        <body>
            <p>Estimado usuario,</p>
            <p>Hemos recibido una solicitud para recuperar la contraseña asociada a este correo electrónico.</p>
            <p>Su código de recuperación es:</p>
            <h2 style="color: #2e6c80;">{code}</h2>
            <p>Por favor, utilice este código para completar el proceso de recuperación de contraseña.</p>
            <p>Si no ha solicitado la recuperación de su contraseña, por favor ignore este correo electrónico.</p>
            <br>
            <p>Gracias por su tiempo,</p>
            <p>El equipo de soporte</p>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, recipient_email, text)
            print('Correo enviado exitosamente!')
            return True, MSG_SUCCESS
        except Exception as e:
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)
        finally:
            server.quit()

    @classmethod
    def update_password(cls, id, new_password):
        try:
            with SessionLocal() as session:
                user = session.query(Credentials).filter(
                    Credentials.id_credencial == id).one_or_none()

                if user:
                    if check_password_hash(user.password, new_password):
                        return False, 'La contraseña ingresada no puede ser igual a la anterior'

                    hashed_password = generate_password_hash(new_password)

                    user.password = hashed_password
                    session.commit()
                    return True, 'Contraseña actualizada exitosamente!'
        except NoResultFound:
            return False, 'No se ha encontrado el usuario en la base de datos'
        except SQLAlchemyError as e:
            print('1')
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)
        except Exception as e:
            print('1')
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)

    @staticmethod
    def log_error(error):
        # Aquí puedes implementar el logging a un archivo o servicio externo
        print(error)

    @classmethod
    def email_blocking_register(cls, id_user):
        try:
            with SessionLocal() as session:
                email_user = session.query(Email).filter(Email.id_user_lock == id_user).first()

                if not email_user:
                    return False, 'No se ha encontrado el usuario en la base de datos'

                # Si attempts ya está en -1, no permitir más envíos
                if email_user.attempts <= 0:
                    return False, 'El envío de códigos está bloqueado. Espere 24 horas para intentar nuevamente.'

                email_user.attempts = email_user.attempts - 1

                if email_user.attempts == 0:
                    email_user.blocking_time = datetime.now(UTC) + timedelta(days=1)
                    session.commit()
                    return True, "Los envíos de mensajes han sido bloqueados. Espere 24 horas para intentar nuevamente."

                session.commit()
                return True, f'Le quedan {email_user.attempts} intentos. De lo contrario, se bloquearán los envíos de mensajes.'
        except NoResultFound:
            return False, 'No se ha encontrado el usuario en la base de datos'
        except SQLAlchemyError as e:
            print('email')
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)
        except Exception as e:
            print('2')
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)

    @classmethod
    def verify_attempts_email(cls, id_user):
        try:
            with SessionLocal() as session:
                user = session.query(Email).filter(Email.id_user_lock == id_user).one_or_none()

                if not user:
                    return False, 'No se ha encontrado el usuario en la base de datos'

                current_time = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')

                if user.attempts <= 0:
                    if user.blocking_time:
                        # Asegurarse de que user.blocking_time sea un objeto datetime
                        blocking_time = user.blocking_time.strftime('%Y-%m-%d %H:%M:%S') if isinstance(user.blocking_time, datetime) else user.blocking_time

                        if blocking_time > current_time:
                            return True, 'El envío de mensajes ha llegado a su límite. Por favor, espere 24 horas y vuelva a intentar.'
                        else:
                            # Reiniciar intentos y tiempo de bloqueo si ha pasado el tiempo de bloqueo
                            user.attempts = 3
                            user.blocking_time = None
                            session.commit()
                            return False, ''
                    else:
                        # Reiniciar intentos si no hay tiempo de bloqueo definido
                        user.attempts = 3
                        session.commit()
                        return False, ''

                return False, ''
        except NoResultFound:
            return False, 'No se ha encontrado el usuario en la base de datos'
        except SQLAlchemyError as e:
            print('3')
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)
        except Exception as e:
            print('3')
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)