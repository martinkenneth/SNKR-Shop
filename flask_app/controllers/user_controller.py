#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import redirect, render_template, request, session
from flask_app import app
from flask_app.models import user
from flask_app.models import sneaker
from flask_bcrypt import Bcrypt
from flask_app import app

# we are creating an object called bcrypt,
# which is made by invoking the function Bcrypt with our app as an argument
bcrypt = Bcrypt(app)


#----------------------------------------------------------------------------#
# User Controllers.
#----------------------------------------------------------------------------#

# View Routes ---------------------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html', sneakers = sneaker.Sneaker.get_all())

@app.route('/register')
def disp_register():
    if 'user_id' in session:
        return redirect('/')
    return render_template('sign_up.html')

@app.route('/login')
def disp_login():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')


# Action Routes -------------------------------------------------------------#
@app.route('/user/register', methods=['POST'])
def register():
    if(user.User.validate_registration(request.form)):
        id = user.User.create(request.form)
        session['user_id'] = id
        return redirect('/')

    return redirect('/register')


@app.route('/user/login', methods=['POST'])
def login():
    if user.User.validate_login(request.form):
        print(session['user_id'])
        return redirect('/')

    return redirect('/login')


@app.route('/user/logout')
def logout():
    print(session)
    session.clear()
    print(session)
    return redirect('/')


#----------------------------------------------------------------------------#
# Error handlers.
#----------------------------------------------------------------------------#
@app.errorhandler(500)
def internal_error(error):
    return "500 error - Internal Error"


@app.errorhandler(404)
def not_found_error(error):
    return "404 error - No Response, page not found"


@app.errorhandler(405)
def not_found_error(error):
    return "405 error - Method Not Allowed (example - trying to [GET] a route that only takes [POST] method"
