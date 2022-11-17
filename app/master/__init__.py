from flask import Blueprint

blueprint = Blueprint(
    'master_blueprint',
    __name__,
    url_prefix='/master'
)

