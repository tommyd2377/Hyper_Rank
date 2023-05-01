## Project Overview

HyperRank is a user-user collaborative filtering algorithm that I have designed for use as a simple recommendation engine and have implemented here in Python.

## HyperRank Function

Mathematically can be written as:

![](https://latex.codecogs.com/svg.image?hr(x)=log\sum_{Uk\varepsilon&space;U}^{Un}((CU\cap&space;Uk)\Re&space;)Un)

where
 
![](https://latex.codecogs.com/svg.image?{X\varepsilon&space;\{TA&space;\vee&space;TB^{2}\vee&space;TC^{3}&space;\})

### Given a set of users and items, represented as user_data and item_data respectively, we can calculate a numerical ranking score for each item using the HyperRank algorithm.
The HyperRank algorithm involves the following steps:
-Assign an integer value to each item based on the number of votes it has received from users.
-Rank the items based on their integer values, with higher values indicating a higher rank.
-Divide the ranked items into three tiers: A, B, and C.
-Apply a scaling factor to the integer values of items in tiers B and C, with the scaling factor increasing for each tier.
-Re-rank the items based on their updated integer values.
-Once the items have been ranked, we can recommend them to a current user based on their past votes.
-The HyperRank class provides methods to perform each of these steps, and the hyper_rank method combines them to generate a ranked list of items that the current user may be interested in.

## Set Partition

Item x is a member of set {T}, which has been partitioned into three subsets {TA, TB, TC} based on the popularity of items within the entire set. Items in {TA} remain unchanged, items in {TB} are squared, and items in {TC} are cubed. {TA} represents the top 25% of most popular items, {TB} represents items between the 25th and 75th percentiles, and {TC} represents the bottom 25%. The purpose of partitioning {T} into three subsets is to provide greater weight to items that are of interest to two users but not generally popular in the set as a whole. This metric significantly increases the similarity between two users when the function is executed.
