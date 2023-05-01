import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def FechaFormato(month):
    Diccionario =  {'01': 'enero', '02': 'febrero',
                    '03': 'marzo','04':'abril',
                    '05': 'mayo', '06':'junio',
                    '07': 'julio','08':'agosto',
                    '09':'septiembre','10':'octubre',
                    '11':'noviembre','12':'diciembre'}
    return Diccionario[month]
     
    
def EnvioEmail(lista_cambios,nombre_cliente,yesterday,sender_email,password,receiver_email,pdfs_radicados):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart("alternative")
    
    message["Subject"] = f"Estados de procesos judiciales Fecha {yesterday}"
    message["From"] = sender_email
    message["To"] = receiver_email
    yesterdat_list = yesterday.split('-')
    year = yesterdat_list[0]
    month = FechaFormato(yesterdat_list[1])
    day_aux = yesterdat_list[2]
    
    if len(day_aux) < 2:
        day = f'0{day_aux}'
    else:
        day = day_aux
        
    message_no = f"""\
        <p style="font-family:courier;">Cordial saludo estimado <b>{nombre_cliente}</b>,<br>
        <br>
        Su aliado DJA, se permite informarle que el día <b>{day}</b> de <b>{month}</b> de <b>{year}</b>, sus procesos 
        <b>NO</b> presentaron nuevas actuaciones. </p>

        <p style="font-family:courier;">Quedamos atentos a cualquier requerimiento adicional.</p>

       <p style="font-family:courier;"> Atentamente,<br> 
        <b>DEPENDENCIA JUDICIAL AUTOMATIZADA</b>
        </p>"""

    table = """ <html>
                <head>
                <style>
                table {
                  font-family: courier, sans-serif;
                  border-collapse: collapse;
                  width: 100%;
                }
                
                td, th {
                  border: 1px solid #dddddd;
                  text-align: left;
                  padding: 8px;
                }
                
                tr:nth-child(even) {
                  background-color: #dddddd;
                }
                </style>
                </head>"""
                
    message_si = f"""\
                 <body>
                 <p style="font-family:courier;"> Cordial saludo estimado <b>{nombre_cliente}</b>,<br>
                 <br>
                 Su aliado DJA, se permite informarle que el día <b>{day}</b> de <b>{month}</b> de <b>{year}</b>, los siguientes procesos presentan nuevas actuaciones:
                 </p>
                 <table>
                  <tr>
                    <th>Radicado</th>
                    <th>Anotación</th>
                    <th>Fecha de Registro</th>
                  </tr>
                  
                  """
    message_si_final  = """\
        </table>
        <p style="font-family:courier;"> Para el efecto, se anexan a este correo los correspondientes Autos.<br> 
        Quedamos atentos a cualquier requerimiento adicional. 
        </p>
        <p style="font-family:courier;"> Atentamente,<br> 
        <b>DEPENDENCIA JUDICIAL AUTOMATIZADA<b>
        </p>
        <body>
        <html>"""
    
    if len(lista_cambios) == 0:
        message_aux = message_no
    else:
        message_si_aux = ''
        for rad in lista_cambios:
            link = pdfs_radicados[rad]
            message_si_aux =  message_si_aux + f"""\
                <tr>
                    <td><a href = {link}>{rad}</a></td>
                    <td>1</td>
                    <td>2</td>
                </tr>
            """
            
        message_aux =table + message_si +message_si_aux +message_si_final
        
    part1 = MIMEText(message_aux, "html")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    
    
