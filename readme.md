## Project Overview

Hyper Rank is user-user collaborative filtering algorithm that I have implemented here in Python. It is designed to 
be extremeley robust even with small inputs so it is an excellent choice for applications with a small dataset. This is still
a work in progress and I'm expolring an implementaion using TensorFlow. 

## Hyper Rank Function

The hyper rank function HR(CU, U, I) -> I' can be defined as follows:

1. Loop through item_data(I) and assign a temporary integer(item_int) to item_data based on vote count
2. Rank items by item_int in descending order
3. Push the top 25% of items into tier_A
4. Push the middle 50% of items into tier_B
5. Push the bottom 25% of items into tier_C
6. Identify the intersection of the current_user(CU) vote array to user_data(U) vote arrays
7. Assign a temporary integer(user_user_int) to each user where an intersection exists
8. Loop through item_data votes array to check if any intersection(user_item_int) with user_user_int exists
9. If intersection exists, loop through user_item_int
10. Subtract the number of user_item_int from the item_int
11. Multiply the items user_item_int by the user_user_int
12. Add the result of step 9 to the result of step 10
13. Log the result of step 11 
14. Loop through items in tier_b and square the item integer
15. Loop through items in tier_c and cube the item integer
16. Rank item_data items by updated integer in descending order
17. Return item_data(I') as dictionary

## Set Partition

Item x is a member of set {T}, which is partitioned into three subsets {TA, TB, TC} based on the items popularity within the entire set. The vote count of items in {TA} are unchanged, items in {TB} are squared, {TC} items are cubed. {TA} respresents items in the top 25% of most popular items, {TB}, between 25% and 75% and {TC}, the bottom 25%. The usefulness of partitioning {T} into three subsets is to give further weight to items that two users have a common interest in but is not generally popular in the set as a whole. This metric adds a much higher degree of similarity between two users when the function is executed.