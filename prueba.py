import requests

username = 'tu_usuario'
password = 'tu_contraseña'
url = 'https://192.168.180.1/login.cgi'

import ssl

context = ssl.create_default_context()
context.options |= ssl.OP_NO_TLSv1_2
context.protocol = ssl.PROTOCOL_TLSv1_1

response = requests.post(url, json={'username': username, 'password': password}, verify=False, ssl_context=context)
if response.status_code == 200:
    print('Autenticación exitosa')
else:
    print('Error al autenticar')