from dataset import user
from dataset import users
from dataset import items

def hyper_rank(current_user, user_data, item_data):

    tier_A = []
    tier_B = []
    tier_C = []

    #loop through item_data and assign a temporary integer to item_data based on raw vote
    for vote_list in item_data:
        vote_list = item_data.votes
        item_int = vote_list.length
        item_data.append(item_int)
        pass

    #rank items by number of votes in descending order
    item_data = sorted(item_data)


    #push the top 25% of items into tier_A
    #push the middle 50% of items into tier_B
    #push the bottom 25% of items into tier_C

    #identify the intersection of the current_user vote array to users_data vote array
    #assign a temporary integer to each user where an intersection exists
    #loop through item_data votes array to check if any intersection uids exist
    #add the user integer - 1 to the item_data integer

    #loop through items in tier_b and square the item integer
    #loop through items in tier_c and cube the item integer

    #rank item_data items by updated integer in descending order
    #return item_data as dictionary

    return item_data

hyper_rank(user, users, items)