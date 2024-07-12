######################################################################## 
# IMPORTS HERE.......................................................... 
######################################################################## 
from flask import Blueprint, render_template 

########################################################################
# CREATING A BLUEPRINT HERE.............................................
########################################################################
career = Blueprint('career', __name__, template_folder='templates', url_prefix='/career') 

########################################################################
# BLUEPRINT ROUTES HERE.................................................
######################################################################## 
@career.route('/', methods=['GET'])
def page():

	return render_template('career/page.jinja2') 

