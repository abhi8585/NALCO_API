from flask import Blueprint

blueprint = Blueprint(
    'loadplanning',
    __name__,
    url_prefix='/loadplanning',
    template_folder='templates',
    static_folder='static'
)

