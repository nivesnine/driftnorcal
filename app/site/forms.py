from wtforms import form, fields, validators
from wtforms.widgets import TextArea


class CommentForm(form.Form):
    comment = fields.StringField('Comment', widget=TextArea(),
                                 validators=[validators.InputRequired()])
    post = fields.HiddenField()
