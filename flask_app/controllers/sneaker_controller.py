#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import render_template
from flask_app import app
from flask_app.models import sneaker


#----------------------------------------------------------------------------#
# Sneaker Controllers.
#----------------------------------------------------------------------------#

# View Routes ---------------------------------------------------------------
@app.route('/sneaker/<int:sneaker_id>')
def disp_sneaker(sneaker_id):
    # check if user is logged in for EACH display route
    data = {
        'id': sneaker_id
    }
    
    return render_template('product_page.html',sneaker = sneaker.Sneaker.get_stock_by_id(data), sneakers = sneaker.Sneaker.get_all())

# Action Routes -------------------------------------------------------------
