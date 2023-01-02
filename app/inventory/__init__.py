from flask import Blueprint

blueprint = Blueprint(
    'inventory',
    __name__,
    url_prefix='/inventory',
    template_folder='templates',
    static_folder='static'
)

