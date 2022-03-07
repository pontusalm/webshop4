from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators
from wtforms.fields import IntegerField, SelectField, BooleanField, SubmitField

class SubscriberNewForm(FlaskForm):
    email = StringField("Email",[validators.Email()])
    submit= SubmitField("Subscribe")

class UserEditForm(FlaskForm):
    first_name = StringField("First name",[validators.Length(min=2, max=20)])
    last_name = StringField("Last name",[validators.Length(min=2, max=25)])

class PasswordEditForm(FlaskForm):
    password = StringField("Enter new password",[validators.Length(min=6, max=255)])
    passwordAgain = StringField("Enter new password again",[validators.Length(min=6, max=255)])

class EmailEditForm(FlaskForm):
    email = StringField("New emailadress",[validators.Email()])
    
class NewNewsletterForm(FlaskForm):
    newsletterTitle = StringField("Please name your newsletter",[validators.Length(min=5, max=50)])
    newsletterText = StringField("Please enter your newsletter-text",[validators.Length(min=120, max=2000)])


    




