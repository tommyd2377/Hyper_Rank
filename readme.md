# Hyper Rank

The hyper rank function HR(CU, U, I) -> I'  can be defined as follows:

1. Loop through item_data(I) and assign a temporary integer to item_data based on raw vote
2. Rank items by number of votes in descending order
3. Push the top 25% of items into tier_A
4. Push the middle 50% of items into tier_B
5. Push the bottom 25% of items into tier_C
6. Identify the intersection of the current_user(CU) vote array to users_data(U) vote array
7. Assign a temporary integer to each user where an intersection exists
8. Loop through item_data votes array to check if any intersection uids exist
9. Add the user integer - 1 to the item_data integer
10. Loop through items in tier_b and square the item integer
11. Loop through items in tier_c and cube the item integer
12. Rank item_data items by updated integer in descending order
13. Return item_data(I') as dictionary

Item x is a member of set { T }, which is partitioned into three subsets { TA, TB, TC } based on the items raw vote count. The vote count of items in TA are unchanged, TB items are squared, TC items are cubed. TA is top 25% most popular items, TB is between 25% and 75% and TC is the bottom 25%. The usefulness of partitioning { T } into three subsets is to give further weight to items that two users have a common interest in but is not generally popular in the network as a whole. This metric adds a much higher degree of similarity between two users.

