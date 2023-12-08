from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup
import requests

# url = 'https://www.wne.uw.edu.pl/'  # Podaj adres strony, którą chcesz zescrapować
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
#
# # Pobierz cały kod HTML strony
# html_content = soup.prettify()
#
# # Zapisz cały kod HTML strony do pliku contact.html w katalogu templates
# with open('templates/contact.html', 'w', encoding='utf-8') as file:
#     file.write(html_content)


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
