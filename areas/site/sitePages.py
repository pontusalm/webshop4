from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_login import login_required, user_logged_in, current_user
from forms import EmailEditForm, PasswordEditForm, SubscriberNewForm, UserEditForm
from models import NewsLetterSubscriber, User, db


siteBluePrint = Blueprint('site', __name__)

@siteBluePrint.route('/contact')
def contact() -> str:
     return render_template('site/contact.html')

@siteBluePrint.route('/terms')
def terms() -> str:
     return render_template('site/terms.html')

@siteBluePrint.route('/about')
def about() -> str:
     return render_template('site/about.html')

@siteBluePrint.route('/profile/<id>',methods=["GET","POST"])
@login_required
def profile(id):

     id= current_user.id
     user = User.query.filter(User.id == id).first()

     return render_template('site/profileEdit.html',user=user)

@siteBluePrint.route('/profileEdit/<id>',methods=["GET","POST"])
def profileEdit(id):

     form = UserEditForm(request.form)
     id= current_user.id
     user = User.query.filter(User.id == id).first()

     if request.method =="GET":
          form.first_name.data = user.first_name
          form.last_name.data = user.last_name
          form.email.data = user.email
          return render_template('site/profileEdit.html',user=user, form=form)



     if form.validate_on_submit():
          user.GivenName = form.first_name.data
          user.Surname = form.last_name.data
          user.Streetaddress = form.email.data


          db.session.commit()
          return redirect(url_for("profileEdit"))
     return render_template('site/profileEdit.html',user=user, form=form)

@siteBluePrint.route('/profileEditInfo/<id>',methods=["GET","POST"])
@login_required
def profileEditInfo(id):

     formInfo = UserEditForm(request.form)
     formPW = PasswordEditForm(request.form)
     formEmail = EmailEditForm(request.form)
     id= current_user.id
     user = User.query.filter(User.id == id).first()

     if request.method =="GET":
          formInfo.first_name.data = user.first_name
          formInfo.last_name.data = user.last_name
          return render_template('site/profileEditInfo.html',formEmail=formEmail, user=user,formPW=formPW, formInfo=formInfo)



     if formInfo.first_name.data and formInfo.validate_on_submit() or formInfo.last_name.data and formInfo.validate_on_submit():
          user.first_name = formInfo.first_name.data
          user.last_name = formInfo.last_name.data
          db.session.commit()
          return redirect(url_for("product.index"))

     elif formEmail.email.data and formEmail.validate_on_submit():
          user.email = formEmail.email.data
          db.session.commit()
          return redirect(url_for("product.index"))

 
     return render_template('site/profileEditInfo.html',user=user,id=id, formEmail=formEmail,formPW=formPW, formInfo=formInfo)





