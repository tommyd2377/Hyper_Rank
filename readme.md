# HyperRank

HyperRank is a small Python implementation of a personalized user-to-user collaborative filtering algorithm. It recommends items to a current user by finding other users with overlapping votes, weighting those overlaps by item popularity tiers, and ranking unseen items by the similarity of the users who voted for them.

The project is intentionally lightweight: there are no external dependencies, no package setup, and no service layer. The core algorithm lives in one file so it is easy to inspect and experiment with.

## Repository Structure

| File | Purpose |
| --- | --- |
| `hyper_rank.py` | Defines the `HyperRank` class and includes a runnable example. |
| `dataset.py` | Provides a small sample dataset using sets for votes. |
| `readme.md` | Explains the algorithm, formulas, data model, and usage. |

## Data Model

HyperRank expects three inputs:

```python
current_user = {
    "uid": "optional-current-user-id",
    "votes": ["item1", "item2"]
}

user_data = [
    {"uid": "user1", "votes": ["item1", "item2", "item4"]},
    {"uid": "user2", "votes": ["item2", "item3", "item5"]}
]

item_data = [
    {"item_id": "item1", "votes": ["user1"]},
    {"item_id": "item2", "votes": ["user1", "user2"]}
]
```

`votes` on a user are item IDs. `votes` on an item are user IDs. Items may use either `item_id` or `id`; the implementation supports both because the example in `hyper_rank.py` uses `item_id` and `dataset.py` uses `id`.

## Algorithm Overview

HyperRank works in four stages:

1. Count how many users voted for each item.
2. Sort items by vote count and divide them into popularity tiers.
3. Score how similar each peer user is to the current user based on shared votes.
4. Recommend unseen items voted for by similar users.

The key idea is that shared interests should not all carry the same weight. The tier transform gives middle and lower popularity tiers a larger exponent before those item weights are used in user similarity.

## Precise Definition

Let:

- $c$ be the current user.
- $U$ be the set of peer user IDs.
- $I$ be the set of items.
- $R_u$ be the set of item IDs voted for by user $u$.
- $V_x$ be the set of user IDs that voted for item $x$.
- $p(x) = |V_x|$ be the raw popularity of item $x$.

Sort all items by descending raw popularity. If the sorted item at zero-based index $j$ is $x_j$, define:

$$
T_A = \{x_j : j < \lfloor |I| / 4 \rfloor\}
$$

$$
T_B = \{x_j : \lfloor |I| / 4 \rfloor \le j < \lfloor 3|I| / 4 \rfloor\}
$$

$$
T_C = \{x_j : \lfloor 3|I| / 4 \rfloor \le j < |I|\}
$$

The tier-adjusted item weight is:

$$
w(x) =
\begin{cases}
p(x), & x \in T_A \\
p(x)^2, & x \in T_B \\
p(x)^3, & x \in T_C
\end{cases}
$$

The similarity between the current user $c$ and a peer user $u$ is:

$$
s(c, u) = \sum_{x \in R_c \cap R_u} w(x)
$$

Only users with $s(c, u) > 0$ are considered similar users.

For an unseen candidate item $y \notin R_c$, define the recommending users:

$$
U_c(y) = \{u \in U : s(c, u) > 0 \land u \in V_y\}
$$

The HyperRank score for item $y$ is:

$$
HR_c(y) = \log \left( \sum_{u \in U_c(y)} s(c, u) \right)
$$

The implementation uses Python's natural logarithm, `math.log`. Candidate items are sorted by descending `hyper_rank_score`, then by descending similarity sum, descending tier-adjusted item weight, and finally by item ID for deterministic tie-breaking.

## How the Code Maps to the Formula

The `HyperRank` class implements the formula through these methods:

| Method | What it does |
| --- | --- |
| `get_item_id` | Reads either `item_id` or `id` from an item dictionary. |
| `assign_item_integers` | Calculates `raw_item_int = p(x)` and initializes `item_int`. |
| `rank_items` | Builds `T_A`, `T_B`, and `T_C`, then calculates `item_int = w(x)`. |
| `score_similar_users` | Calculates $s(c, u)$ for each peer user with overlapping votes. |
| `recommend_items` | Calculates $HR_c(y)$ for unseen items voted for by similar users. |
| `hyper_rank` | Runs the full pipeline and returns ranked recommendations. |

Each returned recommendation includes:

| Field | Meaning |
| --- | --- |
| `raw_item_int` | Raw item popularity, $p(x)$. |
| `item_int` | Tier-adjusted item weight, $w(x)$. |
| `tier` | The item's popularity tier: `A`, `B`, or `C`. |
| `recommended_by` | Similar users who voted for the item. |
| `similarity_sum` | The unlogged sum of recommending-user similarity scores. |
| `hyper_rank_score` | The final logged recommendation score. |

## Running the Project

Use Python 3:

```bash
python3 hyper_rank.py
```

The script runs the inline example in `hyper_rank.py` and prints personalized recommendations for:

```python
current_user = {"votes": ["item1", "item2"]}
```

You can also import the class and use the sample data from `dataset.py`:

```python
from dataset import user, users, items
from hyper_rank import HyperRank

ranked_items = HyperRank().hyper_rank(user, users, items)
print(ranked_items)
```

## Current Behavior and Limitations

HyperRank currently models votes as positive-only signals. It does not distinguish between ratings, dislikes, skips, recency, or confidence levels.

The similarity score is intentionally simple: shared items are summed after the tier transform. There is no normalization for very active users, sparse users, or globally dominant items beyond the current tier weighting.

The implementation is optimized for readability and experimentation, not large-scale recommendation serving. For larger datasets, the next step would be to add indexing, tests, benchmarks, and a clearer input/output API.
