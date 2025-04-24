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
    subject = "⚠️ ALERTA: Ameaça detectada - Arma identificada"

    # Template HTML do email
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f8f8;
                border-radius: 5px;
            }
            .header {
                background-color: #ff4444;
                color: white;
                padding: 15px;
                text-align: center;
                border-radius: 5px 5px 0 0;
                margin-bottom: 20px;
            }
            .content {
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .footer {
                text-align: center;
                font-size: 12px;
                color: #666666;
            }
            .alert-icon {
                font-size: 24px;
                margin-bottom: 10px;
            }
            .timestamp {
                color: #666666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="alert-icon">⚠️</div>
                <h2>ALERTA DE SEGURANÇA</h2>
            </div>
            <div class="content">
                <p><strong>Uma possível ameaça foi detectada pelo sistema de monitoramento.</strong></p>
                <p>Detalhes do alerta:</p>
                <ul>
                    <li>Tipo: Arma detectada</li>
                    <li>Data e hora: {timestamp}</li>
                </ul>
                <p>A imagem abaixo mostra o momento da detecção:</p>
                <img src="cid:imagem_detectada" style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px;">
                <p style="color: #ff4444;"><strong>Por favor, verifique imediatamente e tome as medidas necessárias.</strong></p>
            </div>
            <div class="footer">
                <p>Este é um email automático do Sistema de Detecção de Ameaças. Não responda a este email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart('related')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adiciona a data e hora atual ao template
    from datetime import datetime
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    html_content = html_template.format(timestamp=timestamp)

    # Anexa o conteúdo HTML
    msg.attach(MIMEText(html_content, 'html'))

    ret, img_encoded = cv2.imencode('.jpg', image)
    if ret:
        img_byte_arr = BytesIO(img_encoded)
        img_byte_arr.seek(0)

        img_attachment = MIMEImage(img_byte_arr.read())
        img_attachment.add_header('Content-ID', '<imagem_detectada>')
        msg.attach(img_attachment)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587) 
            server.starttls()
            server.login(from_email, os.environ.get('EMAIL_PASSWORD'))
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f'Ocorreu um erro ao enviar o e-mail: {e}')
    else:
        print("Erro ao codificar a imagem.")
