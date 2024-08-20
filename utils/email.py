from fastapi import HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


def send_registration_email(recipient_email: str, username: str, password: str):
    """Envoie un email de bienvenue avec les informations d'inscription."""
    # Configuration de l'email
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    
    subject = "Réinitialisation de votre mot de passe"

    # Créer le message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject
    body = f"""
    <html>
    <body>
        <h1>Bienvenue sur notre plateforme !</h1>
        <p>Bonjour {username},</p>
        <p>Votre inscription a été réalisée avec succès. Voici vos informations de connexion :</p>
        <ul>
            <li><strong>Email :</strong> {recipient_email}</li>
            <li><strong>Mot de passe :</strong> {password}</li>
        </ul>
        <p>Nous vous recommandons de changer ce mot de passe lors de votre première connexion pour plus de sécurité.</p>
        <p>Merci de nous avoir rejoint !</p>
        <p>Cordialement,<br>L'équipe de support</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Sécuriser la connexion
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'envoi de l'email.")