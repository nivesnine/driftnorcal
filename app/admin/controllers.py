# Import flask dependencies
from datetime import datetime

import flask_login as login
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_admin import helpers
from werkzeug.security import generate_password_hash

from app import db
import app.admin.forms as AdminForms
import app.auth.models as AuthModels
import app.events.models as EventsModels
import app.media.models as MediaModels
from app.helpers.decorators import check_admin, check_login, has_role
from app.helpers.utils import slugify

# Create blog blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/', methods=['GET'])
@check_login
@check_admin
def index():
    return render_template("admin/index.html")


# Create the user routes
@admin.route('/user', defaults={'page': 1}, methods=['GET'])
@admin.route('/user/<int:page>', methods=['GET'])
@check_login
@check_admin
def user_list(page):
    order = 'users_' + request.args[
        'sort'] if 'sort' in request.args else 'users_id'
    direction = request.args['d'] if 'd' in request.args else 'desc'
    users = AuthModels.User.get_sortable_list(order, direction, page)

    return render_template("admin/users/list.html", users=users)


@admin.route('/user/create', methods=['GET', 'POST'])
@check_login
@check_admin
def create_user():
    form = AdminForms.CreateUserForm(request.form)
    if helpers.validate_form_on_submit(form):
        user = AuthModels.User()
        form.populate_obj(user)
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.user_list'))

    return render_template("admin/users/user.html", form=form)


@admin.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit_user(user_id):
    user = AuthModels.User.query.get(user_id)
    old_pass = user.password
    user.password = None
    last_login = user.last_login_ip
    form = AdminForms.EditUserForm(request.form, obj=user)
    if helpers.validate_form_on_submit(form):

        form.populate_obj(user)

        if user.password == '':
            user.password = old_pass
        else:
            user.password = generate_password_hash(user.password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin.user_list'))

    return render_template("admin/users/user.html", form=form,
                           last_login=last_login)


@admin.route('/user/delete/<int:user_id>', methods=['GET'])
@check_login
@check_admin
def delete_user(user_id):
    user = AuthModels.User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.user_list'))


# Create the role routes
@admin.route('/role', defaults={'page': 1}, methods=['GET'])
@admin.route('/role/<int:page>', methods=['GET'])
@check_login
@check_admin
def role_list(page):
    order = request.args['sort'] if 'sort' in request.args else 'id'
    direction = request.args['d'] if 'd' in request.args else 'desc'
    roles = AuthModels.Role.get_sortable_list(order, direction, page)

    return render_template("admin/roles/list.html", roles=roles)


@admin.route('/role/create', methods=['GET', 'POST'])
@check_login
@check_admin
def create_role():
    form = AdminForms.CreateRoleForm(request.form)
    if helpers.validate_form_on_submit(form):
        role = Role()
        form.populate_obj(role)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('admin.role_list'))

    return render_template("admin/roles/role.html", form=form)


@admin.route('/role/edit/<int:role_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit_role(role_id):
    role = AuthModels.Role.query.get(role_id)
    form = AdminForms.EditRoleForm(request.form, obj=role)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(role)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('admin.role_list'))

    return render_template("admin/roles/role.html", form=form)


@admin.route('/role/delete/<int:role_id>', methods=['GET'])
@check_login
@check_admin
def delete_role(role_id):
    role = AuthModels.Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('admin.role_list'))


# Create the event routes
@admin.route('/event', defaults={'page': 1}, methods=['GET'])
@admin.route('/event/<int:page>', methods=['GET'])
@check_login
@check_admin
def event_list(page):
    order = request.args['sort'] if 'sort' in request.args else 'id'
    direction = request.args['d'] if 'd' in request.args else 'desc'
    events = EventsModels.Event.get_sortable_list(order, direction, page)

    return render_template("admin/events/list.html", events=events)


@admin.route('/event/create', methods=['GET', 'POST'])
@check_login
@check_admin
def create_event():
    form = AdminForms.CreateEventForm(request.form)
    if helpers.validate_form_on_submit(form):
        event = EventsModels.Event()
        form.populate_obj(event)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('admin.event_list'))

    return render_template("admin/events/event.html", form=form)


@admin.route('/event/edit/<int:event_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit_event(event_id):
    event = EventsModels.Event.query.get(event_id)
    form = AdminForms.EditEventForm(request.form, obj=event)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(event)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('admin.event_list'))

    return render_template("admin/events/event.html", form=form)


@admin.route('/event/delete/<int:event_id>', methods=['GET'])
@check_login
@check_admin
def delete_event(event_id):
    event = EventsModels.Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('admin.event_list'))


# Create the media routes
@admin.route('/media', defaults={'page': 1}, methods=['GET'])
@admin.route('/media/<int:page>', methods=['GET'])
@check_login
@check_admin
def media_list(page):
    order = request.args['sort'] if 'sort' in request.args else 'id'
    direction = request.args['d'] if 'd' in request.args else 'desc'
    media = MediaModels.Media.get_sortable_list(order, direction, page)

    return render_template("admin/media/list.html", media=media)


@admin.route('/media/create', methods=['GET', 'POST'])
@check_login
@check_admin
def create_media():
    form = AdminForms.CreateMediaForm(request.form)
    if helpers.validate_form_on_submit(form):
        media = MediaModels.Media()
        form.populate_obj(media)
        db.session.add(media)
        db.session.commit()
        return redirect(url_for('admin.media_list'))

    return render_template("admin/media/media.html", form=form)


@admin.route('/media/edit/<int:media_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit_media(media_id):
    media = MediaModels.Media.query.get(media_id)
    form = AdminForms.EditEventForm(request.form, obj=media)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(media)
        db.session.add(media)
        db.session.commit()
        return redirect(url_for('admin.media_list'))

    return render_template("admin/media/media.html", form=form)


@admin.route('/media/delete/<int:media_id>', methods=['GET'])
@check_login
@check_admin
def delete_media(media_id):
    media = MediaModels.Media.query.get_or_404(media_id)
    db.session.delete(media)
    db.session.commit()
    return redirect(url_for('admin.media_list'))
