from bs4 import BeautifulSoup
import requests
# import time
from datetime import datetime
import smtplib
from email.message import EmailMessage

with open('secrets.txt', 'r') as file:
    exec(file.read())

previous_title = 'Pracownicy naukowi i doktoranci WNE UW z grantami w konkursach NCN'


def send_email(receiver_email, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = my_email
    msg['To'] = receiver_email
    msg.set_content(body + f'''
        <!DOCTYPE html>
        <html>
            <body>
                  <p>Aby się wypisać kliknij w 
                  <a href="https://www.wne.uw.edu.pl/members/profile/view/102">link</a>. </p>
            </body>
        </html>
        ''', subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user=my_email, password=my_password)
        connection.send_message(msg)


# Podaje link do nowego artykułu a następnie scrapuje jego tytuł i zawartość
def get_article(article_url):
    try:
        response = requests.get(article_url)
        new_article = response.text

        soup = BeautifulSoup(new_article, "html.parser")

        title = soup.find("h1").getText()
        # print(title)

        content_container = soup.find("div", class_="insideworkzone")

        content = ""

        if content_container:
            text_blocks = content_container.find_all("p")

            for block in text_blocks:
                text = block.getText()
                content += f"{text}\n\n"

        # print(content)

        send_email(receiver, title, content)
    except Exception as e:
        print(f"Błąd podczas pobierania artykułu: {e}")


def scrape_articles(last_title):
    global previous_title
    # Scrappuję tekst strony
    response = requests.get("https://www.wne.uw.edu.pl/")
    wne_web = response.text

    soup = BeautifulSoup(wne_web, "html.parser")

    news_container = soup.find("div", class_="ccm-block-page-list-pages")

    found_new_title = False

    if news_container:
        article = news_container.find("a", target="_self")
        title = article.getText()
        if title != last_title:
            url = article.get("href")
            get_article(url)
            previous_title = title
            found_new_title = True

        if found_new_title:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            print("done!")


scrape_articles(previous_title)
# while True:
#     scrape_articles(previous_title)
#     time.sleep(60)
