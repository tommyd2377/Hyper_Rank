import math
from typing import Any, Dict, List

class HyperRank():
    # Define the HyperRank class, which will contain the functions necessary for ranking the items

    def get_item_id(self, item: Dict[str, Any]) -> str:
        return item.get("item_id", item.get("id"))


    def assign_item_integers(self, item_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        # This function takes in a list of dictionaries, each containing item data and a list of votes.
        # It assigns each item a numerical integer based on the number of votes it has.
        # The updated item data with the integer value is returned as a list of dictionaries.

        updated_item_data = []

        for item in item_data:
            votes = item["votes"]
            item_int = len(votes)
            new_item = dict(item)
            new_item["raw_item_int"] = item_int
            new_item["item_int"] = item_int
            updated_item_data.append(new_item)

        return updated_item_data


    def rank_items(self, item_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        # This function takes in a list of dictionaries containing item data and their assigned integers.
        # It ranks the items into three tiers: A, B, and C based on their assigned integer values.
        # It then modifies the integer values of the items in tier B and tier C.
        # Finally, it returns the sorted list of items based on their modified integer values.

        sorted_items = sorted(item_data, key=lambda x: x["item_int"], reverse=True)
        tier_size = len(item_data) // 4
        tier_c_start = (3 * len(item_data)) // 4
        tier_A = sorted_items[:tier_size]
        tier_B = sorted_items[tier_size:tier_c_start]
        tier_C = sorted_items[tier_c_start:]

        for item in tier_A:
            item["tier"] = "A"

        for item in tier_B:
            item["tier"] = "B"
            item["item_int"] = item["item_int"] ** 2

        for item in tier_C:
            item["tier"] = "C"
            item["item_int"] = item["item_int"] ** 3

        sorted_items = sorted(item_data, key=lambda x: x["item_int"], reverse=True)
        return sorted_items


    def score_similar_users(
        self,
        current_user: Dict[str, Any],
        user_data: List[Dict[str, Any]],
        ranked_items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        # Similar users are weighted by the ranked value of the items they have in common
        # with the current user, so shared niche interests count more than shared popular ones.

        current_user_votes = set(current_user["votes"])
        current_user_id = current_user.get("uid")
        item_scores = {
            self.get_item_id(item): item["item_int"]
            for item in ranked_items
        }
        similar_users = []

        for user in user_data:
            if current_user_id is not None and user.get("uid") == current_user_id:
                continue

            user_votes = set(user["votes"])
            shared_votes = current_user_votes.intersection(user_votes)

            if not shared_votes:
                continue

            similarity_score = sum(
                item_scores.get(item_id, 1)
                for item_id in shared_votes
            )
            similar_user = dict(user)
            similar_user["shared_votes"] = sorted(shared_votes, key=str)
            similar_user["similarity_score"] = similarity_score
            similar_users.append(similar_user)

        return sorted(similar_users, key=lambda user: user["similarity_score"], reverse=True)


    def recommend_items(
        self,
        current_user: Dict[str, Any],
        similar_users: List[Dict[str, Any]],
        ranked_items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        # Each candidate item is scored by summing the similarity of users who voted for it.

        current_user_votes = set(current_user["votes"])
        user_scores = {
            user["uid"]: user["similarity_score"]
            for user in similar_users
        }
        recommendations = []

        for item in ranked_items:
            item_id = self.get_item_id(item)

            if item_id in current_user_votes:
                continue

            similar_voters = sorted(
                set(item["votes"]).intersection(user_scores),
                key=str
            )

            if not similar_voters:
                continue

            similarity_sum = sum(user_scores[uid] for uid in similar_voters)
            recommended_item = dict(item)
            recommended_item["recommended_by"] = similar_voters
            recommended_item["similarity_sum"] = similarity_sum
            recommended_item["hyper_rank_score"] = math.log(similarity_sum)
            recommendations.append(recommended_item)

        return sorted(
            recommendations,
            key=lambda item: (
                -item["hyper_rank_score"],
                -item["similarity_sum"],
                -item["item_int"],
                str(self.get_item_id(item))
            )
        )


    def hyper_rank(self, current_user: Dict[str, Any], user_data: List[Dict[str, Any]], item_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        # This function takes in a dictionary of votes for the current user, a list of dictionaries containing user data,
        # and a list of dictionaries containing item data and their assigned integers. It ranks items, calculates
        # weighted similarity between users, and returns unseen items sorted by personalized HyperRank score.

        item_data = self.assign_item_integers(item_data)
        ranked_items = self.rank_items(item_data)
        similar_users = self.score_similar_users(current_user, user_data, ranked_items)

        return self.recommend_items(current_user, similar_users, ranked_items)


if __name__ == "__main__":
    # example usage
    hr = HyperRank()

    # Create an example current user dictionary and example lists of user and item dictionaries
    current_user = {"votes": ["item1", "item2"]}

    user_data = [
        {"uid": "user1", "votes": ["item1", "item2", "item4"]},
        {"uid": "user2", "votes": ["item2", "item3", "item5"]},
        {"uid": "user3", "votes": ["item3", "item4", "item6"]},
        {"uid": "user4", "votes": ["item1", "item3", "item5", "item6"]},
        {"uid": "user5", "votes": ["item2", "item4", "item6"]}
    ]

    item_data = [
        {"item_id": "item1", "votes": ["user1", "user4"]},
        {"item_id": "item2", "votes": ["user1", "user2", "user5"]},
        {"item_id": "item3", "votes": ["user2", "user3", "user4"]},
        {"item_id": "item4", "votes": ["user1", "user3", "user5"]},
        {"item_id": "item5", "votes": ["user2", "user4"]},
        {"item_id": "item6", "votes": ["user3", "user4", "user5"]}
    ]

    # call the hyper_rank() function and store the result in the variable ranked_items
    ranked_items = hr.hyper_rank(current_user, user_data, item_data)
    # print the ranked_items to the console
    print(ranked_items)
