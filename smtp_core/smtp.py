import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class smtpConfig:
    port = 587
    smtp_server = "smtp.free.fr"
    login = "codebara"  # Votre identifiant généré par Mailtrap
    password = "Alexmivaimk5#"  # Votre mot de passe généré par Mailtrap
    sender_email = "codebara@free.fr"

def mailto(dest,messageText,subject):
  
    config=smtpConfig()
    # Créer un objet MIMEText
    message = MIMEText(messageText, "plain")
    message["Subject"] = subject
    message["From"] = config.sender_email
    message["To"] = dest

    # Envoyer l'email
    with smtplib.SMTP(config.smtp_server, config.port) as server:
        server.starttls()  # Sécuriser la connexion
        print(server.login(config.login, config.password))
        ret=server.sendmail(config.sender_email, dest, message.as_string())
        print(ret)
        print('Envoyé à '+dest)

def mailtoHTML(dest,messageHTML,subject):
    config=smtpConfig()
    
    # Créer un objet MIMEText
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = config.sender_email
    message["To"] = dest

    # Joindre la partie HTML
    message.attach(MIMEText(messageHTML, "html"))

    # Envoyer l'email
    with smtplib.SMTP(config.smtp_server, config.port) as server:
        server.starttls()
        server.login(config.login, config.password)
        ret=server.sendmail(config.sender_email, dest, message.as_string())
        print(ret)
        print('Envoyé')