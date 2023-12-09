from flask import Flask, render_template, request, redirect, url_for
from functions import send_email, signup, signout, validation

app = Flask(__name__)

# with open('templates/confirmation.html', 'r', encoding='utf-8') as file:
#     content = file.read()
title = "Potwierdź swój email"
content = "hello suer"


@app.route('/')
def contact():
    return render_template('contact.html')


@app.route('/signup', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('user_email')
        return redirect(url_for('confirmation', email=email))
    else:
        return redirect(url_for('contact'))


@app.route('/confirmation/<email>')
def confirmation(email):
    if validation(email):
        send_email(email, title, content, "confirmation")
        return f"Wysłaliśmy mail z potwierdzeniem na adres: {email}"
    else:
        return redirect(f'/failed/{email}')


@app.route('/thankyou/<email>')
def thank_you(email):
    if validation(email):
        signup(email)
        return "Dziękujemy za potwierdzenie maila!"
    else:
        return redirect(f'/failed/{email}')


@app.route('/signout/<email>')
def sign_out(email):
    signout(email)
    return f"Potwierdzamy wypisanie {email}"


@app.route('/failed/<email>')
def failed(email):
    return f"{email} jest już zapisany do newslettera"


if __name__ == '__main__':
    app.run(debug=True)
