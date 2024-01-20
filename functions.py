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


def validation(email):
    email = email.lower()
    # Wczytanie istniejących adresów e-mail z pliku CSV
    try:
        with open('email_list.csv', 'r') as file:
            reader = csv.reader(file)
            emails = [row[0].strip().lower() for row in reader if row]  # Pominięcie pustych wierszy
    except FileNotFoundError:
        emails = []

    # Sprawdzenie, czy adres e-mail znajduje się na liście
    if email in emails:
        return False
    else:
        return True


def signup(email, frequency):
    try:
        with open('email_list.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, frequency])  # Zapis dwóch wartości oddzielnie
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


def send_mail_with_frequency(receiver_email, frequency, body):

    with open('email_list.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

    if frequency == 'daily':
        body = reader
    elif frequency == 'weekly':
        pass
    elif frequency == 'monthly':
        pass
    else:
        pass

    try:
        msg = MIMEMultipart()
        msg['Subject'] = f'Your {frequency} newsletter is here!'
        msg['From'] = my_email
        msg['To'] = receiver_email
    except smtplib.SMTPRecipientsRefused as e:
        print(f"Recipient email refused: {e}")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")


def send_email(receiver_email, subject, body, style_type):
    try:
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
    except smtplib.SMTPRecipientsRefused as e:
        print(f"Recipient email refused: {e}")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")


# Podaje link do nowego artykułu a następnie scrapuje jego tytuł i zawartość
def get_article(article_url):
    try:
        response = requests.get(article_url)
        new_article = response.text

        soup = BeautifulSoup(new_article, "html.parser")

        # scrapowanie zawartości artykułu
        title = soup.find("h1").getText()
        # print(title)

        content_container = soup.find("div", class_="insideworkzone")

        content = ""

        if content_container:
            text_blocks = content_container.find_all("p")

            for block in text_blocks:
                text = block.getText()
                content += f"{text}\n\n"

        scraped_date = soup.find("div", class_="ccm-custom-style-header16")
        clean_date = scraped_date.getText().strip().split(',')[0]
        print(clean_date)

        # print(content)

        # Jeśli użytkownik ma częstotliwość ustawioną na 'up to date' wysyłamy mu zawartość artykułu na tym poziomie
        with open('email_list.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                email = row[0]
                frequency = row[1]
                if frequency == 'up to date':
                    send_email(email, title, content, "mail")

        # process_emails()
    except Exception as e:
        print(f"Błąd podczas pobierania artykułu: {e}")


def scrape_articles():
    # Scrapujemy tekst strony
    response = requests.get("https://www.wne.uw.edu.pl/")
    wne_web = response.text

    soup = BeautifulSoup(wne_web, "html.parser")

    # Wybieramy container w którym znajdują się artykuły
    news_container = soup.find("div", class_="ccm-block-page-list-pages")

    found_new_title = False

    # Zapisujemy tytuły z pliku csv do listy jako previous_titles
    if news_container:
        articles = news_container.find_all("a", target="_self")
        previous_titles = []
        with open('previous_titles.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                title = row[1]
                previous_titles.append(title)

        # Zczytujemy datę publikacji, tytyuł artykułu i jego url a następnie sprawdzamy czy artykuł był już wpisany na \
        # listę, jeśli nie to jest dopisywany.
        for article in articles:
            article_title = article.getText()
            # print(article_title)
            url = article.get("href")
            # print(url)
            response = requests.get(url)
            new_article = response.text
            soup2 = BeautifulSoup(new_article, "html.parser")
            scraped_date = soup2.find("div", class_="ccm-custom-style-header16")
            clean_date = scraped_date.getText().strip().split(',')[0]
            # print(clean_date)
            row_data = [clean_date, article_title, url]
            if article_title not in previous_titles:
                get_article(url)
                with open('previous_titles.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(row_data)

    #     if article_title != previous_title:
    #         url = article.get("href")
    #         get_article(url)
    #         with open('previous_title.txt', 'w', encoding='utf-8') as file1:
    #             file1.write(article_title)
    #         found_new_title = True
    #
    #     if found_new_title:
    #         print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    #         print("done!")


if __name__ == "__main__":
    # process_emails()
    scrape_articles()

# while True:
#     scrape_articles(previous_title)
#     time.sleep(60)
