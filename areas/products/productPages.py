from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import current_user
from .services import getCategory, getTrendingCategories, getProduct, getTrendingProducts
from forms import SubscriberNewForm
from models import NewsLetterSubscriber, User
from models import db

productBluePrint = Blueprint('product', __name__)

@productBluePrint.route('/', methods=["GET", "POST"])
def index() -> str:
    if current_user.is_authenticated:
        print(current_user.email)
    trendingCategories = []
    trendingCategories = getTrendingCategories()
    trendingProducts = getTrendingProducts()

    # Subscribing newsletter.
    form=SubscriberNewForm()

    # Checking if current logged in user is subscriber
    isNewsletterSubscriber=True
    if current_user.is_authenticated:

        if NewsLetterSubscriber.query.filter_by(email=current_user.email).first():
            isNewsletterSubscriber=False
    isNLSubscriber={"isNewsletterSubscriber":isNewsletterSubscriber}

    if request.method == "GET":
        return render_template('products/index.html',trendingCategories=trendingCategories, products=trendingProducts, isNLSubscriber=isNLSubscriber, form=form)


    if form.is_submitted:
        if form.validate_on_submit():
            if NewsLetterSubscriber.query.filter_by(email=form.email.data).first():
                flash("You are already a subsciber of the newsletter")
                return redirect(url_for("product.index"))
            nlsubscriber=NewsLetterSubscriber(email=form.email.data)
            db.session.add(nlsubscriber)
            db.session.commit()
            flash("Thanks for subscribing")
            return redirect(url_for("product.index"))
        else:
            flash("You have entered an invalid email, please try again.")

    return render_template('products/index.html',trendingCategories=trendingCategories, products=trendingProducts,isNLSubscriber=isNLSubscriber ,form=form)



@productBluePrint.route('/category/<id>')
def category(id) -> str:
    category = getCategory(id)
    return render_template('products/category.html',category=category)

@productBluePrint.route('/product/<id>')
def product(id) -> str:
    product = getProduct(id)
    return render_template('products/product.html',product=product)


