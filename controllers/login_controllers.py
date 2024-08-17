import os
import smtplib
import pytz
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import and_
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
import logging

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
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Date and Time
UTC = pytz.timezone("America/Caracas")

# Configuración de logging
logging.basicConfig(filename='application.log', level=logging.ERROR)

class LoginController:
    @classmethod
    def authenticate(cls, username, password):
        """Autentica el usuario y la contraseña en la base de datos"""
        if not username or not password:
            return False, 'warning', 'Por favor ingrese usuario y contraseña.'

        try:
            with SessionLocal() as session:
                result = session.query(Credentials).filter(Credentials.id_username == username).one_or_none()
                if result and check_password_hash(result.password, password):
                    return result.fk_user_id, result.position, MSG_SUCCESS
                return False, 'warning', MSG_INVALID_CREDENTIALS
        except SQLAlchemyError as e:
            cls.log_error(e)
            return False, 'critical', MSG_UNEXPECTED_ERROR.format(e)

    @classmethod
    def forgot_password(cls, user_id, email):
        """Verifica si el correo electrónico existe en la base de datos"""
        if not email:
            return False, 'warning', 'Por favor ingrese un correo electrónico.'

        try:
            with SessionLocal() as session:
                result = session.query(User).filter(
                    and_(User.id_user == user_id, User.email == email)
                ).one_or_none()

                if result:
                    return True, result.email, MSG_SUCCESS
                return False, 'warning', MSG_INVALID_EMAIL
        except SQLAlchemyError as e:
            cls.log_error(e)
            return False, 'critical', MSG_UNEXPECTED_ERROR.format(e)

    @classmethod
    def send_email(cls, code, email):
        """Envía un correo electrónico con el código de recuperación"""
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

        msg = cls.create_email_message(SENDER_EMAIL, email, subject, body)

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, email, msg.as_string())
                print('Correo enviado exitosamente!')
                return True, MSG_SUCCESS
        except Exception as e:
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)

    @staticmethod
    def create_email_message(sender_email, recipient_email, subject, body):
        """Crea un mensaje de correo electrónico"""
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, 'html'))
        return msg

    @classmethod
    def update_password(cls, user_id, new_password):
        """Actualiza la contraseña del usuario"""
        try:
            with SessionLocal() as session:
                user = session.query(Credentials).filter(Credentials.id_credencial == user_id).one_or_none()

                if user and not check_password_hash(user.password, new_password):
                    user.password = generate_password_hash(new_password)
                    session.commit()
                    return True, 'Contraseña actualizada exitosamente!'
                return False, 'La contraseña ingresada no puede ser igual a la anterior'
        except SQLAlchemyError as e:
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)

    @classmethod
    def email_blocking_register(cls, user_id):
        """Registra un intento de envío de correo y gestiona el bloqueo si es necesario"""
        try:
            with SessionLocal() as session:
                email_user = session.query(Email).filter(Email.id_user_lock == user_id).first()

                if not email_user:
                    return False, 'No se ha encontrado el usuario en la base de datos'

                if email_user.attempts <= 0:
                    return False, 'El envío de códigos está bloqueado. Espere 24 horas para intentar nuevamente.'

                email_user.attempts -= 1

                if email_user.attempts == 0:
                    email_user.blocking_time = datetime.now(UTC) + timedelta(days=1)
                    session.commit()
                    return True, "Los envíos de mensajes han sido bloqueados. Espere 24 horas para intentar nuevamente."

                session.commit()
                return True, f'Le quedan {email_user.attempts} intentos. De lo contrario, se bloquearán los envíos de mensajes.'
        except SQLAlchemyError as e:
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)

    @classmethod
    def verify_attempts_email(cls, user_id):
        """Verifica los intentos restantes para el envío de correos y gestiona el desbloqueo si es necesario"""
        try:
            with SessionLocal() as session:
                user = session.query(Email).filter(Email.id_user_lock == user_id).one_or_none()

                if not user:
                    return False, 'No se ha encontrado el usuario en la base de datos'

                current_time = datetime.now(UTC)

                if user.attempts <= 0:
                    if user.blocking_time and user.blocking_time > current_time:
                        return True, 'El envío de mensajes ha llegado a su límite. Por favor, espere 24 horas y vuelva a intentar.'
                    else:
                        # Reiniciar intentos y tiempo de bloqueo si ha pasado el tiempo de bloqueo
                        user.attempts = 3
                        user.blocking_time = None
                        session.commit()
                        return False, ''
                return False, ''
        except SQLAlchemyError as e:
            cls.log_error(e)
            return False, MSG_UNEXPECTED_ERROR.format(e)

    @staticmethod
    def log_error(error):
        """Registra los errores en un archivo log"""
        logging.error(error)

