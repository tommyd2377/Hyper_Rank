from dataset import user as cu
from dataset import users as u
from dataset import items as i

class HyperRank():

    def hyper_rank(self, current_user, user_data, item_data):

        tier_A = set()
        tier_B = set()
        tier_C = set()

        #loop through item_data and assign a temporary integer to item_data based on raw vote
        for item in item_data:
            print("item: ", item["votes"])
            votes = item["votes"]
            item_int = len(votes)
            item["item_int"] = item_int

        #rank items by number of votes in descending order
        item_data = sorted(item_data, 'votes', True)

        #tier items
        item_data_quarter = len(item_data) / 4
        item_count = 0

        for item in item_data:
            #push the top 25% of items into tier_A
            if item_count < item_data_quarter:
                tier_A.add(item)
                item_count = item_count + 1
            #push the bottom 25% of items into tier_C
            elif item_count > item_data_quarter * 3:
                tier_C.add(item)
                item_count = item_count + 1
            #push the middle 50% of items into tier_B
            else:
                tier_B.add(item)
                item_count = item_count + 1

        #identify the intersection of the current_user vote array to users_data vote array
        current_user_votes = current_user["votes"]
        intersection_users = set()
        for user in user_data:
            user_votes = user["votes"]
            vote_intersection = current_user_votes.intersection(user_votes)
            #assign a temporary integer to each user where an intersection exists
            if len(vote_intersection) > 0:
                temp_int = len(vote_intersection)
                uid = user["uid"]
                intersection_user = {}
                intersection_user["temp_int"] = temp_int
                intersection_user["uid"] = uid
                intersection_users.add(intersection_user)
            
        #loop through item_data votes array to check if any intersection uids exist
        item_intersections = []
        for item in item_data:
            item_vote = item["votes"]
            for uids in intersection_users:
                user_uid = uids["uid"]
                user_int = uids["temp_int"]
                if user_uid == item_vote:
                    item_vote_length = len(item_vote)
                    item_vote_length = item_vote_length + user_int
           
        #add the user integer - 1 to the item_data integer

        #loop through items in tier_b and square the item integer
        #loop through items in tier_c and cube the item integer

        #rank item_data items by updated integer in descending order
        #return item_data as dictionary

hr = HyperRank()
print(hr.hyper_rank(cu, u, i))