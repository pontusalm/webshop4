from asyncio.windows_events import NULL
from flask import Flask, redirect, render_template, request, url_for
from forms import NewNewsletterForm
from models import Newsletter, db, seedData
from models import db, seedData, User, user_manager
from flask_migrate import Migrate, upgrade
from areas.site.sitePages import siteBluePrint
from areas.products.productPages import productBluePrint
from flask_user import current_user, roles_required
from areas.api.apiMain import apiListSubscriberBlueprint, apiSubscribeBlueprint, apiUnSubscribeBlueprint

app = Flask(__name__)

app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)
# user_manager.app = app
# user_manager.init_app(app,db,User)
user_manager.app = app
user_manager.init_app(app, db, User)


@app.route("/createnewsletter", methods=["GET", "POST"])
@roles_required("Admin")
def createNewsletterPage():
    form = NewNewsletterForm(request.form)

    if request.method == "GET":
        return render_template('createnewsletter.html', form=form)

    if form.validate_on_submit():
        newNewsletter = Newsletter()
        newNewsletter.title = form.newsletterTitle.data
        newNewsletter.text = form.newsletterText.data
        db.session.add(newNewsletter)
        db.session.commit()
        return redirect(url_for('newslettersPage'))

    return render_template('newsletterlist.html', form=form)


@app.route("/newsletters", methods=["GET", "POST"])
@roles_required("Admin")
def newslettersPage():
    sortColumn = request.args.get('sortColumn', 'Id')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))

    searchWord = request.args.get('q', '')

    activePage = "newsletterPage"
    allNewsletters = Newsletter.query.filter(
        Newsletter.id.like('%' + searchWord + '%') |
        Newsletter.title.like('%' + searchWord + '%') |
        Newsletter.sent.like(searchWord))

    if sortColumn == "id":
        if sortOrder == "desc":
            allNewsletters = allNewsletters.order_by(Newsletter.id.desc())
        else:
            allNewsletters = allNewsletters.order_by(Newsletter.id.asc())

    if sortColumn == "Titel":
        if sortOrder == "desc":
            allNewsletters = allNewsletters.order_by(Newsletter.title.desc())
        else:
            allNewsletters = allNewsletters.order_by(Newsletter.title.asc())

    if sortColumn == "Skickat":
        if sortOrder == "desc":
            allNewsletters = allNewsletters.order_by(Newsletter.sent.desc())
        else:
            allNewsletters = allNewsletters.order_by(Newsletter.sent.asc())

    paginationObject = allNewsletters.paginate(page, 20, False)

    return render_template('newsletterlist.html',
                           allNewsletters=paginationObject.items,
                           page=page,
                           sortColumn=sortColumn,
                           sortOrder=sortOrder,
                           q=searchWord,
                           has_next=paginationObject.has_next,
                           has_prev=paginationObject.has_prev,
                           pages=paginationObject.pages,
                           activePage=activePage)


app.register_blueprint(siteBluePrint)
app.register_blueprint(productBluePrint)
app.register_blueprint(apiSubscribeBlueprint)
app.register_blueprint(apiUnSubscribeBlueprint)
app.register_blueprint(apiListSubscriberBlueprint)

if __name__ == "__main__":
    with app.app_context():
        upgrade()
        seedData()
    app.run(debug=True)
