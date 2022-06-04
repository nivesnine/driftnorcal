from flask import (
    Blueprint, request, render_template,
    redirect, url_for, abort, jsonify
)
import app.events.models as EventsModels
from app import db

events = Blueprint('events', __name__, url_prefix='/events')


@events.route('/', methods=['GET'])
def index():
    events = EventsModels.Event.get_upcoming()
    if request.args.get('ajax'):
        data = []
        for event in events:
            if event.price is 0:
                price = ''
            else:
                price = "$" + str(event.price)

            data_set = [event.name,
                event.date.strftime("%m/%d/%Y (%A)"),
                event.host,
                event.location,
                price]

            data_set.append(render_template('/events/view_event.html',
                event_id=event.id))

            data.append(data_set)

        return jsonify({'data': data})
    return render_template("/events/index.html", events=events)


@events.route('/event/<int:event_id>', methods=['GET'])
def event(event_id):
    event = EventsModels.Event.query.get(event_id)
    return render_template("/events/event.html", event=event)
