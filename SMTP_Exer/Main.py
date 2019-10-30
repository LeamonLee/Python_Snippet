import smtplib
 
# 輸入gmail信箱的資訊
host = "smtp.gmail.com"
port = 587
username = "leamon.lee@pioneerm.com"
password = "ihzxoalkvutseqnq"
from_email = username
to_list = ["leamon.lee13@gmail.com"]
 
# 建立SMTP連線
email_conn = smtplib.SMTP(host,port)
 
# 試試看能否跟Gmail Server溝通
print("Connection: ", email_conn.ehlo())
 
# TTLS安全認證機制
email_conn.starttls()
 
try:
    # 登錄Gmail
    print("Loggin status: ", email_conn.login(username,password))
    # 寄信
    email_conn.sendmail(from_email, to_list, "Hello World, I am here!!")
except smtplib.SMTPAuthenticationError:
    print("Could not login")
except:
    print("an error occured!")


# 關閉連線
email_conn.quit()