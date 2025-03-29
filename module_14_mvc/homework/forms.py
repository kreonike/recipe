from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
