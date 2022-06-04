from wtforms import form, fields, validators
from wtforms.widgets import TextArea
from wtforms_alchemy import QuerySelectMultipleField, QuerySelectField
import app.auth.models as AuthModels


def roles():
    return AuthModels.Role.all()


class CreateUserForm(form.Form):
    email = fields.StringField('Email', validators=[validators.InputRequired()])
    password = fields.StringField('Password')

    roles = QuerySelectMultipleField('User Roles', query_factory=roles,
                                     allow_blank=False)

    active = fields.BooleanField()
    submit = fields.SubmitField('Submit')


class EditUserForm(CreateUserForm):
    id = fields.HiddenField()
    roles = QuerySelectMultipleField('User Roles', query_factory=roles,
                                     allow_blank=False)


class CreateRoleForm(form.Form):
    name = fields.StringField('Name', validators=[validators.InputRequired()])
    description = fields.StringField('Description', validators=[validators.InputRequired()])
    submit = fields.SubmitField('Submit')


class EditRoleForm(CreateRoleForm):
    id = fields.HiddenField()


class CreateEventForm(form.Form):
    name = fields.StringField('Name', validators=[validators.InputRequired()])
    date = fields.DateField('Start', validators=[validators.InputRequired()])
    host = fields.StringField('Host', validators=[validators.InputRequired()])
    location = fields.StringField('Location', validators=[validators.InputRequired()])
    price = fields.IntegerField('Price', validators=[validators.InputRequired()])
    details = fields.TextAreaField('Details', validators=[validators.InputRequired()])
    submit = fields.SubmitField('Submit')


class EditEventForm(CreateEventForm):
    id = fields.HiddenField()
