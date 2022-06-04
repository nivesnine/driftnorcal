from flask import Blueprint, render_template

site = Blueprint('site', __name__, url_prefix='')


@site.route('/', methods=['GET'])
def index():
    return render_template("/site/index.html")
