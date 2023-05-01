## Project Overview

Hyper Rank is a user-user collaborative filtering algorithm that I have implemented here in Python.

## Hyper Rank Function

Mathematically can be written as:

![](http://www.sciweavers.org/tex2img.php?eq=hr%28%20%5Cchi%20%29%20%3D%20log%5Csum_%7BU%20%5Ckappa%20%20%5Cepsilon%20U%7D%5E%7BUn%7D%20%28%28%7BCU%7D%20%7B%5Cbigcap_%7D%20%7BU%20%5Ckappa%20%7D%29%20%5CRe%20%29Un&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

Given a set of users and items, represented as user_data and item_data respectively, we can calculate a numerical ranking score for each item using the HyperRank algorithm.
The HyperRank algorithm involves the following steps:
Assign an integer value to each item based on the number of votes it has received from users.
Rank the items based on their integer values, with higher values indicating a higher rank.
Divide the ranked items into three tiers: A, B, and C.
Apply a scaling factor to the integer values of items in tiers B and C, with the scaling factor increasing for each tier.
Re-rank the items based on their updated integer values.
Once the items have been ranked, we can recommend them to a current user based on their past votes.
The HyperRank class provides methods to perform each of these steps, and the hyper_rank method combines them to generate a ranked list of items that the current user may be interested in.
