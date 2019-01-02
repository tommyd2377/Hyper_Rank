# Hyper Rank

The hyper rank function HR(CU, U, I) -> I'  can be defined as follows:

Item x is a member of set { T }, which is partitioned into three subsets { TA, TB, TC } based on the items raw vote count. The vote count of items in TA are unchanged, TB items are squared, TC items are cubed. TA is top 25% most popular items, TB is between 25% and 75% and TC is the bottom 25%. The usefulness of partitioning { T } into three subsets is to give further weight to items that two users have a common interest in but is not generally popular in the network as a whole.