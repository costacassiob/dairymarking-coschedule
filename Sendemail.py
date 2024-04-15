import smtplib
import email.message

def enviar_email(destinatario, login_usu, senha_usu, password):  # Alterando o nome do parâmetro para evitar conflito de nomes
    corpo_email = """
    <h2>Ol&aacute;, bom dia!</h2>
    <h2>Hello, good morning!</h2>
    <p>&nbsp;</p>
    <p>Segue sua se&ccedil;&atilde;o e senha para acesso e recupera&ccedil;&atilde;o do relat&oacute;rio de datas dispon&iacute;veis. Compartilhe a sua se&ccedil;&atilde;o com as pessoas que voc&ecirc; deseja que participem da escolha das datas.</p>
    <p>Here is your section and password for accessing and recovering the available dates report. Share your section with the people you want to participate in choosing the dates.</p>
    <p><strong>SEÇÃO: """+ login_usu +"""</strong></p>
    <p><strong>PASSOWORD: """+ senha_usu + """</strong></p>
    <p>&nbsp;</p>
    <address>Abra&ccedil;os fraternos!</address>
    <address>Fraternity hugs!</address>
    """

    msg = email.message.Message()
    msg['Subject'] = "CoSchedule - New Section"
    msg['From'] = 'costa.bcassio@gmail.com'
    msg['To'] = destinatario  # Usando o email fornecido como destinatário 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
