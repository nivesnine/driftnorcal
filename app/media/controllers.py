from flask import (
    Blueprint, request, render_template,
    redirect, url_for, abort,
)
import app.media.models as MediaModels
from app import db

media = Blueprint('media', __name__, url_prefix='/media')


@media.route('/', methods=['GET'])
def index():
    return render_template("/media/index.html")
