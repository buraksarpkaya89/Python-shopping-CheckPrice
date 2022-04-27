from requests import get
from parsel   import Selector
from smtplib  import SMTP, SMTPException
from CONFIG   import HEADER, MAIL_ADDR, MAIL_PASS, RECIEVER
from schedule import every, run_pending

URL   = None
DEGER = None

def check_price() -> None:
    global URL, DEGER

    if not URL:
        URL = input('Urun linkini giriniz : ')

    product_page = get(URL, headers=HEADER)
    select       = Selector(product_page.text)

    title = select.xpath("normalize-space(//*[contains(@id, 'product-name')])").get()
    print(f"\n{title}")

    price = float(select.xpath("//*[contains(@id, 'offering-price')]/@content").get())
    print(price)

    if not DEGER:
        DEGER = float(input('\nHangi fiyattan asagi dusmesini istiyorsunuz : '))

    if (price < DEGER):
        send_mail(title, price)

def send_mail(product:str, price:float) -> None:

    try:
        mail_server = SMTP('smtp.gmail.com', 587, timeout=60)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.login(MAIL_ADDR, MAIL_PASS)

        subject = f"{product} Urun Fiyat Dustu. Yeni Fiyat : {price}"
        body    = f"Urune bu linkten gidebilirsin => {URL}"
        content = f"To:{RECIEVER}\nFrom:{MAIL_ADDR}\nSubject:{subject}\n\n{body}"

        mail_server.sendmail(MAIL_ADDR, RECIEVER, content)

        print('Mail Gonderildi!')
    except SMTPException as e:
        print(e)
    finally:
        mail_server.quit()

if __name__ == '__main__':
    check_price()

    every(1).hours.do(check_price)

    while True:
        run_pending()