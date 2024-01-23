from flask import Flask, render_template, request, redirect, url_for
from functions import send_confirmation_email, signup, signout, validation

app = Flask(__name__)

# Strona główna z zapisem
@app.route('/')
def contact():
    return render_template('main_page.html')

# Strona zbierająca email z froma przekierowuje od razu na confirmation
@app.route('/signup', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('user_email')
        return redirect(url_for('confirmation', email=email))
    else:
        return redirect(url_for('contact'))


# Jeśli validacja maila udana wysyłamy maila z potwierdzeniem
@app.route('/confirmation/<email>')
def confirmation(email):
    if validation(email):
        send_confirmation_email(email)
        message = "Wysłaliśmy email z potwierdzeniem na adres: "
        return render_template('content.html', message=message, email=email)
    else:
        return redirect(f'/failed/{email}')


# Jeśli wszystko jej poprawnie zapisujemy potwierdzonego maila na listę i przekierowujemy na stronę z podziękowaniem
@app.route('/thankyou/<email>')
def thank_you(email):
    if validation(email):
        signup(email)
        message = "Dziękujemy za potwierdzenie maila!"
        return render_template('content.html', message=message)
    else:
        return redirect(f'/failed/{email}')


# Strona wykonuje funkcję wypisania użytkownika i pokazuje komunikat z jego potwierdzeniem
@app.route('/signout/<email>')
def sign_out(email):
    signout(email)
    message = "Potwierdzamy wypisanie: "
    return render_template('content.html', message=message, email=email)


# Strona domyślna jeśli coś poszło nie tak przy zapisywaniu
@app.route('/failed/<email>')
def failed(email):
    message = "Podany adres jest już zapisany do newslettera: "
    return render_template('content.html', message=message, email=email)


if __name__ == '__main__':
    app.run(debug=True)
