from flask import (
    Blueprint, request, render_template,
    redirect, url_for, abort,
)
import app.shops.models as ShopsModels
from app import db

shops = Blueprint('shops', __name__, url_prefix='/shops')


@shops.route('/', methods=['GET'])
def index():
    return render_template("/shops/index.html")
