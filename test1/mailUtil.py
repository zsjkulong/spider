import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import operator
class mailUtil:
    path = 'D:/test.xlsx';
    sender = 'zsjkulong@163.com'
    sendFlag = 'true'
    #sender = '53353752@QQ.com'
    #sender = '18980438873m@sina.cn'
    receivers = ''  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #receiversArray = ['zsjkulong@163.com'];
    def sendMail(self):

        if(operator.eq(self.sendFlag,'false')):
            return;

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header("股票数据from", 'utf-8')
        message['To'] = Header("股票数据to", 'utf-8')
        subject = '股票数据'
        message['Subject'] = Header(subject, 'utf-8')



        # 邮件正文内容
        message.attach(MIMEText('股票数据', 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下的 test.txt 文件
        att1 = MIMEText(open(self.path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="stock.xlsx"'
        message.attach(att1)

        #try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect('smtp.163.com', 25)
        #smtpObj.connect('smtp.sina.com', 25)
        #smtpObj.connect('smtp.qq.com', 25)  # 25 为 SMTP 端口号
        smtpObj.login('zsjkulong@163.com', '123456Qq')

        for str1 in self.receivers.split(','):
            smtpObj.sendmail(self.sender,str1, message.as_string())

        print('邮件发送成功')
        # except smtplib.SMTPException:
        #     print(smtplib.SMTPException)
