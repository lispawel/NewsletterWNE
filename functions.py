import time
from scraper import Scraper
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Wczytujemy my_email i my_password z pliku secrets.txt
with open('secrets.txt', 'r') as file:
    exec(file.read())

scraper = Scraper(my_email=my_email, my_password=my_password)


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
        # Zapisuję nowego maila do pliku
        with open('email_list.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email])
    except Exception as e:
        print(f"Wystąpił problem podczas zapisu adresu {email}: {e}")


def signout(email):
    try:
        email = email.lower()

        # Wczytanie istniejących e-maili z pliku CSV
        with open('email_list.csv', 'r') as file:
            reader = csv.reader(file)
            emails = [row[0].strip() for row in reader]

        # Sprawdzenie, czy adres e-mail znajduje się na liście
        if email in emails:
            emails = [row for row in emails if row != email]

            # Zapisanie zaktualizowanych danych z powrotem do pliku CSV
            with open('email_list.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([[row] for row in emails])

    except Exception as e:
        return f"Wystąpił błąd: {e}. Spróbuj ponownie później."


def send_confirmation_email(receiver_email):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = "Potwierdź swój email"
        msg['From'] = my_email
        msg['To'] = receiver_email

        with open(f'templates/confirmation.html', 'r', encoding='utf-8') as mail_file:
            html_content = mail_file.read()
        message = MIMEText(html_content.format(user_email=receiver_email), 'html', 'utf-8')

        msg.attach(message)

        with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
            connection.login(user=my_email, password=my_password)
            connection.send_message(msg)
    except Exception as e:
        print(f"An error occurred while sending email to {receiver_email}: {e}")


# Scrapowanie co minute
if __name__ == "__main__":
    while True:
        scraper.scrape_articles()
        time.sleep(60)
