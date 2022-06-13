from datetime import datetime
from xmlrpc.client import DateTime
from django.contrib import messages

from auctions.models import Comment, Listing


def update_watchlist(is_watched, user, listing):
    if not is_watched: # add the listing to watchlist
        listing.watchers.add(user)
        is_watched = True
    else: # remove from the listing to watchlist
        listing.watchers.remove(user)
        is_watched = False

def submit_bid(request, listing, user):
    bid = float(request.POST["bid"])
    # set restrictions for new bid
    previous_bid = listing.current_bid
    if bid > previous_bid:
        listing.current_bid = bid
        listing.current_bidder = user
        listing.save()
        messages.success(request, 'Successfully bid.')
    else:
        messages.warning(request, 'Invalid bid.')

def submit_comment(request, listing, user):
    text = request.POST["comment"]
    comment = Comment(
        commentor = user,
        comment_content = text,
        date = datetime.now,
        listing = listing
        )
    comment.save()
    listing.comments.add(comment)

# retreive all categories to a list 
def get_categories():
    # add all the categories into a list
    categories = set()
    for c in Listing.CATEGORY_CHOICES:
        categories.add(c[0])
    return categories