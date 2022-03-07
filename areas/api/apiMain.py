from asyncio.windows_events import NULL
from flask import Blueprint, redirect, render_template, flash, url_for, request, jsonify
from models import db, NewsLetterSubscriber
import re
from .apiServices import getSubscribers

apiSubscribeBlueprint = Blueprint('apiSubscribe', __name__)
apiUnSubscribeBlueprint = Blueprint('apiUnsubscribe', __name__)
apiListSubscriberBlueprint = Blueprint('apiListSubs', __name__)


def checkMail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False


@apiSubscribeBlueprint.route('/api/newsletter/subscribe/<email>', methods=["GET"])
def apiNewSubscriptionPage(email):
    if checkMail(email) == True:
        newSubscriber = NewsLetterSubscriber()
        newSubscriber.active = 1
        newSubscriber.email = email
        newSubscriber.first_name = ""
        newSubscriber.last_name = ""
        findUser = NewsLetterSubscriber.query.filter_by(email=email).first()
        if findUser is None:
            db.session.add(newSubscriber)
            db.session.commit()
            return render_template('/api/Subscribe.html', email=email)
        else:
            return render_template('/api/Error.html', email=email)
    else:
        return render_template('/api/Error.html', email=email)


@apiUnSubscribeBlueprint.route('/api/newsletter/unsubscribe/<email>', methods=["GET"])
def apiNewSubscriptionPage(email):
    unsubscriber = NewsLetterSubscriber.query.filter_by(email=email).first()
    if unsubscriber is not None:
        db.session.delete(unsubscriber)
        db.session.commit()
        return render_template('/api/Unsubscribe.html', email=email)
    else:
        return render_template('/api/Error.html', email=email)

        # /api/newsletter/listsubscribers?top=5&skip=2


@apiListSubscriberBlueprint.route('/api/newsletter/listsubscribers', methods=["GET"])
def apiGetSubscriberList():
    startOfList = int(request.args['skip'])
    Amount = int(request.args['top'])

    paginateSubscribers = getSubscribers(startOfList, Amount)
    per_page = 5
    page = int(request.args.get('page', 1))
    paginateSubscribers = paginateSubscribers.paginate(
        page=page, per_page=per_page)

    has_next_page = paginateSubscribers.has_next
    has_prev_page = paginateSubscribers.has_prev
    return render_template('/api/listsubscribers.html', pagination=paginateSubscribers.items, has_next_page=has_next_page, startOfList=startOfList, Amount=Amount, has_prev_page=has_prev_page, page=page)
