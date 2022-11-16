from flask import Blueprint

blueprint = Blueprint(
    'modify',
    __name__,
    url_prefix='/modify',
    template_folder='templates',
    static_folder='static'
)

