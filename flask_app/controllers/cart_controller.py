#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import redirect, render_template, request, session
from flask_app import app
from flask_app.models import sneaker
from flask_app.models import user


#----------------------------------------------------------------------------#
# Sneaker Controllers.
#----------------------------------------------------------------------------#

# View Routes ---------------------------------------------------------------
@app.route('/cart')
def disp_cart():
    if 'user_id' not in session:
        return redirect('/register')

    data = {
        'id' : session['user_id']
    }
    user_= user.User.get_users_cart(data)
    total = 0
    if user_:
        for item in user_.cart:
            total += item.price
    print(total)
    return render_template('cart.html', user=user_, total=total)


@app.route('/cart/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect('/register')

    data = {
        'id' : session['user_id']
    }

    if not user.User.get_users_cart(data):
        return redirect('/')

    user_= user.User.get_users_cart(data)
    total = 0
    if user_:
        for item in user_.cart:
            total += item.price

    return render_template('checkout.html', user=user_, total=total)

# Action Routes -------------------------------------------------------------
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    print(request.form)
    sneaker.Sneaker.add_to_cart(request.form)
    return redirect('/cart')

@app.route('/cart/delete/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    print(request.form)
    data = {
        'id' : cart_id
    }
    sneaker.Sneaker.delete_from_cart(data)
    return redirect('/cart')
    # data = {
    #     'id' : session['user_id']
    # }
    # user_=user.User.get_users_cart(data)
    # total = 0
    # for item in user_.cart:
    #     total += item.price
    # print(total)
