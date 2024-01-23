import csv
import requests
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, my_email, my_password):
        self.my_email = my_email
        self.my_password = my_password

    def send_email(self, receiver_email, subject, body):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.my_email
            msg['To'] = receiver_email

            # Wczytuję zawartość html i formatuję do niego dane dynamicznie
            with open(f'templates/mail.html', 'r', encoding='utf-8') as mail_file:
                html_content = mail_file.read()
            message = MIMEText(html_content.format(body_content=body, user_email=receiver_email), 'html', 'utf-8')

            msg.attach(message)

            with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
                connection.login(user=self.my_email, password=self.my_password)
                connection.send_message(msg)
        except Exception as e:
            print(f"An error occurred while sending email to {receiver_email}: {e}")

    def get_article(self, article_url):
        try:
            # Podaje link do nowego artykułu a następnie scrapuje jego tytuł i zawartość
            response = requests.get(article_url)
            new_article = response.text

            soup = BeautifulSoup(new_article, "html.parser")

            # Zapisuję tytuł artykułu
            title = soup.find("h1").getText()

            content_container = soup.find("div", class_="insideworkzone")

            content = ""

            # Zapisuję zawartość artykułu
            if content_container:
                text_blocks = content_container.find_all("p")

                for block in text_blocks:
                    text = block.getText()
                    content += f"{text}\n\n"

            # Iteruję po mailach zapisanych do newslettera i dla każdego wykonuję funkcję send_email()
            try:
                with open('email_list.csv', mode='r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            receiver = row[0]
                            self.send_email(receiver, title, content)
            except Exception as e:
                print(f"An error occurred during sending email: {e}")

        except Exception as e:
            print(f"An error occurred during getting article: {e}")

    def scrape_articles(self):
        try:
            # Odczytuję tytuł ostatniego wysłanego artykułu i zapisuję do zmiennej
            with open('previous_title.txt', 'r', encoding='utf-8') as title:
                previous_title = title.read()

            # Scrappuję tekst strony
            response = requests.get("https://www.wne.uw.edu.pl/")
            wne_web = response.text

            soup = BeautifulSoup(wne_web, "html.parser")

            news_container = soup.find("div", class_="ccm-block-page-list-pages")

            found_new_title = False

            # Jeśli container nie jest pusty, zapisuję najnowszy tytuł artykułu,
            # Jeśli jest to nowy artykuł, który nie był jeszcze wysłany, zapisuję jego url i wykonuję funkcję get_article
            # a następnie zamieniam nowy tytuł w pliku
            if news_container:
                article = news_container.find("a", target="_self")
                article_title = article.getText()
                if article_title != previous_title:
                    url = article.get("href")
                    self.get_article(url)
                    with open('previous_title.txt', 'w', encoding='utf-8') as file:
                        file.write(article_title)
                    found_new_title = True

                if found_new_title:
                    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    print("done!")

        except Exception as e:
            print(f"An error occurred during scraping: {e}")
