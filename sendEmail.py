# coding:utf8

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class SendEmail:
    def __init__(self):
        self.user = None
        self.passwd = None
        self.to_list = []
        self.cc_list = []
        self.tag = None
        self.doc = None

    def send(self, html):
        """
        发送邮件
        """
        try:
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
            server.login(self.user, self.passwd)
            server.sendmail("<%s>" % self.user, self.to_list, self.get_attach(html))
            server.close()
            print("send email successful")
        except Exception as e:
            print("send email failed %s" % e)

    def get_attach(self,html):
        """
        构造邮件内容
        """
        attach = MIMEMultipart()
        html_txt = MIMEText(html,'html','utf-8')
        attach.attach(html_txt)
        if self.tag is not None:
            # 主题,最上面的一行
            # if not isinstance(self.tag,unicode):
                # subject = unicode(self.tag)
                # attach["Subject"] = subject
            attach["Subject"] = self.tag.encode('utf-8')
            #attach["Subject"] = self.tag
        if self.user is not None:
            # 显示在发件人
            attach["From"] = "<%s>" % self.user
        if self.to_list:
            # 收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            # 抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            # 估计任何文件都可以用base64，比如rar等
            # 文件名汉字用gbk编码代替
            name = os.path.basename(self.doc).encode("gbk")
            f = open(self.doc, "rb")
            doc = MIMEText(f.read(), "base64", "gb2312")
            doc["Content-Type"] = 'application/octet-stream'
            doc["Content-Disposition"] = 'attachment; filename="' + name + '"'
            attach.attach(doc)
            f.close()
        return attach.as_string()


if __name__ == "__main__":
    test = SendEmail()

    test.user = "youremail@xxx.com"
    test.passwd = "XXXXXXXXXXXXXXXx"
    test.to_list = ["xxxx@xxx.com", ]
    test.cc_list = ["xxxx@xxx.com", ]
    test.tag = "xxxxxxxxxxxxx"
    test.doc = u"/opt/local/html/xxxxx/xxxxxxxx.html"
    test.send("hhhhhhh")

