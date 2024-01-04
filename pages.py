from flask import Flask, render_template, request, redirect, url_for
from functions import send_email, signup, signout, validation

app = Flask(__name__)


@app.route('/')
def contact():
    return render_template('main_page.html')


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
        title = "Potwierdź swój email"
        with open('templates/confirmation.html', 'r', encoding='utf-8') as file:
            content = file.read()
        send_email(email, title, content, "confirmation")
        message = "Wysłaliśmy email z potwierdzeniem na adres: "
        return render_template('content.html', message=message, email=email)
    else:
        return redirect(f'/failed/{email}')


@app.route('/thankyou/<email>')
def thank_you(email):
    return render_template('frequency.html', user_email=email)


@app.route('/signup2/<email>', methods=['POST'])
def sign_up2(email):
    if request.method == 'POST':
        frequency = request.form.get('frequency')
        if validation(email):
            signup(email, frequency)
            return redirect('/fuckyou/')
        else:
            return redirect(f'/failed/{email}')
    else:
        return redirect(url_for('contact'))


@app.route('/fuckyou/')
def fuck_you():
    message = "Dziękujemy za potwierdzenie maila!"
    return render_template('content.html', message=message)


@app.route('/signout/<email>')
def sign_out(email):
    signout(email)
    message = "Potwierdzamy wypisanie: "
    return render_template('content.html', message=message, email=email)


@app.route('/failed/<email>')
def failed(email):
    message = "Podany adres jest już zapisany do newslettera: "
    return render_template('content.html', message=message, email=email)


if __name__ == '__main__':
    app.run(debug=True)
