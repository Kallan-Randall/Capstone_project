from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = IntegerField('Category', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients  = TextAreaField('Ingredients ', validators=[DataRequired()])
    instructions  = TextAreaField('Instructions ', validators=[DataRequired()])
    cooking_time  = IntegerField('Cooking Time ', validators=[DataRequired()])
    picture = StringField('Picture link')
    submit = SubmitField('Submit Recipe')