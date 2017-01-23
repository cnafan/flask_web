import threading
from flask_mail import Mail, Message

def send_async_email(self,msg):
    mail = Mail(app)
    mail.send(msg)
class Email():
        

    def send_email(self,recipients):
        msg = Message("验证账户", sender ='sikuquanshu123@163.com' , recipients = recipients)
        msg.body = 'dDear,</p><p>Welcome to <b>Flasky</b>!</p><p>To confirm your account please <a href="www.qianggege.cn/confirm", token=token, _external=True)">click here</a>.Sincerely,</p><p>The Flasky Team</p><p><small>Note: replies to this email address are not monitored.</small>'
        msg.html = '<p>body</p>'
        thr = threading.Thread(target = send_async_email, args = [msg])
        thr.start()

        
