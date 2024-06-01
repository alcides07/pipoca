import smtplib
from decouple import config
from fastapi import HTTPException, status
from email.mime.text import MIMEText


def send_email(
    remetente: str,
    destinatario: str,
    assunto: str,
    corpo: str
):
    try:
        producao = int(config("PRODUCAO", default=0))
        if (producao):
            mensagem = MIMEText(corpo, "html")
            mensagem['From'] = remetente
            mensagem['Subject'] = assunto
            mensagem['To'] = destinatario
            PASSWORD_EMAIL = str(config("PASSWORD_EMAIL"))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(remetente, PASSWORD_EMAIL)
                smtp_server.sendmail(
                    from_addr=remetente,
                    to_addrs=destinatario,
                    msg=mensagem.as_string()
                )

        return

    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro ao enviar o e-mail de confirmação!"
        )
