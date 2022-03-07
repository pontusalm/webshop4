from models import NewsLetterSubscriber


# def getSubscribers(amountToList, startOfList):
#     allSubscribers = NewsLetterSubscriber.query.all()
#     subscribersToGet = allSubscribers[startOfList:(amountToList+startOfList)]
#     return subscribersToGet


def getSubscribers(startOfList, Amount):
    maxId = startOfList+Amount
    allSubscribers = NewsLetterSubscriber.query.filter(
        NewsLetterSubscriber.id >= startOfList, NewsLetterSubscriber.id <= maxId)
    return allSubscribers
