from flask import (
    Blueprint, request, render_template,
    redirect, url_for, abort, jsonify
)
import app.media.models as MediaModels
from app import db

media = Blueprint('media', __name__, url_prefix='/media')


@media.route('/', methods=['GET'])
def index():
    media = MediaModels.Media.all()
    if request.args.get('ajax'):
        data = []
        for m in media:

            data_set = []

            data_set.append(render_template('/media/instagram.html',
                instagram=m.instagram))
            data_set.append(render_template('/media/website.html',
                website=m.website))
            data_set.append(m.locations)
            data_set.append(m.types)

            data.append(data_set)

        return jsonify({'data': data})
    return render_template("/media/index.html", media=media)
