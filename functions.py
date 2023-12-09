from bs4 import BeautifulSoup
import requests
# import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import csv

with open('secrets.txt', 'r') as file:
    exec(file.read())

previous_title = 'Pracownicy naukowi i doktoranci WNE UW z grantami w konkursach NCN'


def validation(email):
    email = email.lower()
    # Wczytanie istniejących e-maili z pliku CSV
    with open('email_list.csv', 'r') as file:
        reader = csv.reader(file)
        emails = [row[0].strip() for row in reader]

    # Sprawdzenie, czy adres e-mail znajduje się na liście
    if email in emails:
        return False
    else:
        return True


def signup(email):
    try:
        with open('email_list.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email])
        return True
    except Exception as e:
        print(f"Wystąpił problem podczas zapisu adresu e-mail: {e}")
        return False


def signout(email):
    email = email.lower()
    # Wczytanie istniejących e-maili z pliku CSV
    with open('email_list.csv', 'r') as file:
        reader = csv.reader(file)
        emails = [row[0].strip() for row in reader]

    # Sprawdzenie, czy adres e-mail znajduje się na liście
    if email in emails:
        emails = [row for row in emails if row != email]  # Usunięcie adresu e-mail

        # Zapisanie zaktualizowanych danych z powrotem do pliku CSV
        with open('email_list.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([[row] for row in emails])
        return f"Usunięto {email} z listy subskrybentów."
    else:
        return f"Adres e-mail {email} nie istnieje na liście subskrybentów."


def send_email(receiver_email, subject, body, style_type):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = my_email
    msg['To'] = receiver_email

    with open(f'templates/{style_type}.html', 'r', encoding='utf-8') as mail_file:
        html_content = mail_file.read()
    # Ustawienie kodowania znaków na utf-8
    message = MIMEText(html_content.format(body_content=body, user_email=receiver_email), 'html', 'utf-8')

    msg.attach(message)

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

        send_email(receiver, title, content, "mail")
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


if __name__ == "__main__":
    scrape_articles(previous_title)

# while True:
#     scrape_articles(previous_title)
#     time.sleep(60)
