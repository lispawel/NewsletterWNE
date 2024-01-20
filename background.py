from datetime import datetime
import time
import csv
from functions import send_email, get_article


def get_frequency_articles(user_email):
    style_type = "mail"

    today = datetime.today()
    formatted_date = today.strftime("%d.%m.%Y")
    print(formatted_date)

    with open('previous_titles.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            email = row[0]
            article_date = row[0]
            user_frequency = row[1]
            subject = f"Your {user_frequency} newsletter is here!"

            if user_frequency == 'up to date':
                pass
            elif user_frequency == 'daily':
                body = reader
                send_email(user_email, subject, body, style_type)
            elif user_frequency == 'weekly':
                pass
            elif user_frequency == 'monthly':
                pass
            else:
                pass


if __name__ == '__main__':
    # while True:
    with open('email_list.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            email = row[0]
            frequency = row[1]
            # print(f"Email with {frequency} frequency: {email}")
            get_frequency_articles(email, frequency)
