## Project Overview

Hyper Rank is a user-user collaborative filtering algorithm that I have implemented here in Python. It is designed to 
be extremely robust even with small inputs so it is an excellent choice for applications with a small dataset. This is still
a work in progress and I'm expolring an implementaion using TensorFlow. 

## Hyper Rank Function

This is the mathematical notaion:

![](http://www.sciweavers.org/tex2img.php?eq=hr%28%20%5Cchi%20%29%20%3D%20log%5Csum_%7BU%20%5Ckappa%20%20%5Cepsilon%20U%7D%5E%7BUn%7D%20%28%28%7BCU%7D%20%7B%5Cbigcap_%7D%20%7BU%20%5Ckappa%20%7D%29%20%5CRe%20%29Un&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

where
 
![](http://www.sciweavers.org/tex2img.php?eq=%20%5Cchi%20%20%5Cepsilon%20%5Cbig%5C%7BTA%5Cbig%5C%20%7B%5Cbigvee_%7D%20%7BTB%5E%7B2%7D%7D%20%5Cbig%5C%20%5Cbigvee_%7D%20TC%5E%7B3%7D%5Cbig%5C%7D%20&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)


The hyper_rank function in Python HR(CU, U, I) -> I' can be defined as follows:

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
12. Add the result of step 10 to the result of step 11
13. Log the result of step 12
14. Loop through items in tier_b and square the item integer
15. Loop through items in tier_c and cube the item integer
16. Rank item_data items by updated integer in descending order
17. Return item_data(I') as dictionary

## Set Partition

Item x is a member of set {T}, which is partitioned into three subsets {TA, TB, TC} based on the items popularity within the entire set. The vote count of items in {TA} are unchanged, items in {TB} are squared, {TC} items are cubed. {TA} respresents items in the top 25% of most popular items, {TB}, between 25% and 75% and {TC}, the bottom 25%. The usefulness of partitioning {T} into three subsets is to give further weight to items that two users have a common interest in but is not generally popular in the set as a whole. This metric adds a much higher degree of similarity between two users when the function is executed.
