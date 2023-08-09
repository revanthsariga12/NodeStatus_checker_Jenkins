from jenkinsapi.jenkins import Jenkins
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


username = "YOUR_JENKINS_USERNAME" #jenkins username
password = "YOUR_JENKINS PASSWORD OR API TOKEN" #created a api token or we can use a password
jenkins = Jenkins('https://localhost:8080/', username=username, password=password)


sender_email = 'SENDER_MAIL'
sender_password = 'SENDER_MAIL_PASSWORD'
receiver_email = 'RECEIVER_MAIL'
subject = 'Jenkins node status'

#To get the status of the given nodes in the list
def get_status():
    node_names = ['AWS-Mac-metal2-FSA-iOS-GO-iOS-Android','AWS-Mac.metal2-Zinc-All', 'AWS-Mac.metal2-Engage', 'AWS-Mac2', 'MacStadium', 'MacStadium_Engage', 'AWS-DCx-Windows', 'AWS_Zinc_Windows_Node','AWS_MFL_Node', 'jenkins-engage-slave', 'MFL-Node', 'MFL-Node2' ]
    L = []
    for node_name in node_names:
        node = jenkins.get_node(node_name)
        if node.is_online():
            L.append((node_name, "Online"))
        else:
            L.append((node_name, "Offline"))
    return(L)
print(get_status())

def send_email(message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Jenkins Node Status Report'

    msg.attach(MIMEText(message, 'html'))
    try:
        smtp_server = smtplib.SMTP('smtp.office365.com, 587)
        smtp_server.starttls()
        smtp_server.login(sender_password, sender_password)
        smtp_server.send_message(msg)
        smtp_server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email. Error: {str(e)}')

#Generating content of the mail and table with dynamic data 
def generate_html_table(data):

    content = f""" \n\n
    <html>
    <head> </head>
    <body>
    <p> Hi Team, <br>
        Please find the status of the nodes: </p> 
    </body>
    </html>
    """
    table = "<table border='1'>"
    table += "<tr><th>Node Name</th><th>Status</th></tr>"
    for node_name, status in data:
        if status == 'Online':
            row = f"<tr><td>{node_name}</td><td style='background-color: green;'>{status}</td></tr>"
        else:
            row = f"<tr><td>{node_name}</td><td style='background-color: red;'>{status}</td></tr>"
        table += row
        #table += f"<tr><td>{node_name}</td><td>{status}</td></tr>"
    table += "</table>"

    greetings = f""" \n\n
    <html>
    <head> </head>
    <body>
    <p> Regards, <br>
        Sariga Revanth </p>
    </body>
    </html> """
    return content + table + greetings

node_status = get_status()
html_table = generate_html_table(node_status)
send_email(html_table)
