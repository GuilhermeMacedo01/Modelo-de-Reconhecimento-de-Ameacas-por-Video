import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
import cv2
from dotenv import load_dotenv

dotenv_path = '/Users/guilherme.macedo/ArmedPeopleDetecter/Modelo-de-Reconhecimento-de-Ameacas-por-Video/email.env'
load_dotenv(dotenv_path)

def send_email_with_image(image):
    """ Envia um e-mail com a imagem anexada usando SMTP """

    from_email = os.environ.get('EMAIL') 
    to_email = os.environ.get('SEND_EMAIL') 
    subject = "Ameaça detectada: Arma identificada"
    body = "A imagem abaixo mostra uma possível ameaça. Verifique imediatamente."

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    ret, img_encoded = cv2.imencode('.jpg', image)
    if ret:
        img_byte_arr = BytesIO(img_encoded)
        img_byte_arr.seek(0)

        img_attachment = MIMEImage(img_byte_arr.read(), name="imagem_detectada.jpg")
        msg.attach(img_attachment)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587) 
            server.starttls()
            server.login(from_email,os.environ.get('EMAIL_PASSWORD'))
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f'Ocorreu um erro ao enviar o e-mail: {e}')
    else:
        print("Erro ao codificar a imagem.")
