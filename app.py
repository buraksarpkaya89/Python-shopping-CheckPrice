import requests
from bs4 import BeautifulSoup
import smtplib
import time

url = input('Urun linkini giriniz ')

headers= {'User-Agent' : 'my user agent(google)'}
def check_price():
    page = requests.get(url,headers=headers)
    soup =BeautifulSoup(page.content,'html.parser')
    title = soup.find(id ='product-name').get_text().strip()
    print(title)
    span = soup.find(id ='offering-price')
    content = span.attrs.get('content')
    price = float(content)
    print(price)
    deger = float(input('Hangi fiyattan asagi dusmesini istiyorsunuz '))
    
    if(price<deger):
        send_mail(title,content)
        
    

def send_mail(title,content):
    sender = 'mail_adresiniz@gmail.com'
    reciever = input('Email Adresini Giriniz ')
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(sender,'gmail app password')
        subject = title + ' ' + 'Urun Fiyat Dustu. Yeni Fiyat :' + ' ' + content 
        body = 'Urune bu linkten gidebilirsin' + ' => ' +url
        mailContent = f"To:{reciever}\nFrom:{sender}\nSubject:{subject}\n\n{body}"
        server.sendmail(sender,reciever,mailContent)
        print('Mail Gonderildi')
    except smtplib.SMTPException as e:
        print(e)
        
    finally:
        server.quit()
        
while(1):
    check_price()
    time.sleep(60*60)