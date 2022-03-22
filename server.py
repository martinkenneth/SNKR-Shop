from flask_app import app
from flask_app.controllers import user_controller
from flask_app.controllers import sneaker_controller
from flask_app.controllers import cart_controller


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:

if __name__ == "__main__":
    app.run(debug=True)
