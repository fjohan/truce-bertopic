import pandas as pd
import numpy as np

def get_topic_tree(
        hier_topics: pd.DataFrame,
        max_distance: float = None,
        tight_layout: bool = False,
        # NEW:
        list_groups: bool = False,
        include_leaves: bool = False,
        unique: bool = True,
        indent_output: bool = False,
        label_sep: str = "_",
    ) -> str:
    """
    Extract the topic tree such that it can be printed.

    Arguments:
        hier_topics: A dataframe containing the structure of the topic tree.
                     This is the output of `topic_model.hierarchical_topics()`
        max_distance: The maximum distance between two topics. This value is
                      based on the Distance column in `hier_topics`.
        tight_layout: Whether to use a tight layout (narrow width) for
                      easier readability if you have hundreds of topics.

        list_groups (NEW): If True, return a flat list of aggregated label groups
                           ordered by depth (root-most first). Keeps original
                           tree traversal order within the same depth.
        include_leaves (NEW): When list_groups=True, also include leaf topics
                              ("■── ... ── Topic: N") in the list.
        unique (NEW): When list_groups=True, de-duplicate labels, keeping the
                      first occurrence.
        indent_output (NEW): When list_groups=True, indent each line by depth.
        label_sep (NEW): When list_groups=True, replace '_' with this separator.

    Returns:
        If list_groups=False (default): Same ASCII tree as the original function.
        If list_groups=True: A newline-joined string of labels ordered by depth,
                             most general first.

    Examples:
    ```python
    # Train model
    from bertopic import BERTopic
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(docs)
    hierarchical_topics = topic_model.hierarchical_topics(docs)

    # 1) Original tree
    tree = topic_model.get_topic_tree(hierarchical_topics)
    print(tree)

    # 2) Aggregated groups, ordered by hierarchy depth
    groups = topic_model.get_topic_tree(hierarchical_topics, list_groups=True)
    print(groups)
    ```
    """
    width = 1 if tight_layout else 4
    if max_distance is None:
        max_distance = hier_topics.Distance.max() + 1
    max_original_topic = hier_topics.Parent_ID.astype(int).min() - 1

    # Extract mapping from ID to name
    topic_to_name = dict(zip(hier_topics.Child_Left_ID, hier_topics.Child_Left_Name))
    topic_to_name.update(dict(zip(hier_topics.Child_Right_ID, hier_topics.Child_Right_Name)))
    topic_to_name = {str(topic): name[:100] for topic, name in topic_to_name.items()}

    # Create tree {Parent_ID: [Left_ID, Right_ID]}
    tree = {
        str(row.Parent_ID): [str(row.Child_Left_ID), str(row.Child_Right_ID)]
        for _, row in hier_topics.iterrows()
    }

    # Helper to fetch merge distance for a given parent id
    def _merge_distance(parent_id: str) -> float:
        m = hier_topics.loc[
            (hier_topics.Child_Left_ID.astype(str) == parent_id) |
            (hier_topics.Child_Right_ID.astype(str) == parent_id),
            "Distance",
        ]
        return float(m.values[0]) if len(m) > 0 else 10.0

    # NEW: we’ll collect rows (depth, label, is_leaf, parent_id, distance)
    collected = []

    def get_tree(start, tree):
        """Based on: https://stackoverflow.com/a/51920869/10532563."""
        def _tree(to_print, start, parent, tree, grandpa=None, indent="", depth=0):
            # distance between merged topics
            distance = _merge_distance(parent)

            if parent != start:
                if grandpa is None:
                    # root label (top aggregated node)
                    to_print += topic_to_name.get(parent, str(parent))
                    # collect aggregated root
                    collected.append((depth, topic_to_name.get(parent, str(parent)), False, parent, distance))
                else:
                    if int(parent) <= max_original_topic:
                        # Leaf/original topic
                        if distance < max_distance:
                            label = topic_to_name.get(parent, str(parent))
                            to_print += "■──" + label + f" ── Topic: {parent}" + "\n"
                            # collect leaf if requested
                            collected.append((depth, label, True, parent, distance))
                        else:
                            to_print += "O \n"  # pruned by distance
                    else:
                        # Aggregated (non-leaf) node
                        lbl = topic_to_name.get(parent, str(parent))
                        to_print += lbl + "\n"
                        collected.append((depth, lbl, False, parent, distance))

            if parent not in tree:
                return to_print

            # left (all but last)
            for child in tree[parent][:-1]:
                to_print += indent + "├" + "─"
                to_print = _tree(to_print, start, child, tree, parent,
                                 indent + "│" + " " * width, depth + 1)
            # right (last)
            child = tree[parent][-1]
            to_print += indent + "└" + "─"
            to_print = _tree(to_print, start, child, tree, parent,
                             indent + " " * (width + 1), depth + 1)
            return to_print

        to_print = "." + "\n"
        to_print = _tree(to_print, start, start, tree, depth=0)
        return to_print

    start = str(hier_topics.Parent_ID.astype(int).max())
    ascii_tree = get_tree(start, tree)

    if not list_groups:
        return ascii_tree

    # ---- Post-process to produce flat, depth-ordered label list ----
    rows = collected

    # Filter leaves if not requested
    if not include_leaves:
        rows = [r for r in rows if not r[2]]  # is_leaf == False

    # Filter out pruned leaves ("O") implicitly by only collecting real labels above

    # De-duplicate on label (keep first occurrence)
    if unique:
        seen = set()
        dedup = []
        for depth, label, is_leaf, pid, dist in rows:
            key = (label, is_leaf)
            if key in seen:
                continue
            seen.add(key)
            dedup.append((depth, label, is_leaf, pid, dist))
        rows = dedup

    # Sort: smaller depth (higher up) first; keep traversal order within same depth
    # Python's sort is stable, so we only sort by depth
    rows.sort(key=lambda x: x[0])

    # Format output
    lines = []
    for depth, label, is_leaf, pid, dist in rows:
        show = label.replace("_", label_sep)
        if indent_output:
            lines.append(("  " * depth) + show)
        else:
            lines.append(show)

    return "\n".join(lines)



def show_top_topics_for_doc(topic_model, doc, top_n=5, top_terms=5):
    """
    Given a fitted BERTopic model and a document, compute the topic distribution
    and print the top-N topics with their probabilities and representative terms.

    Args:
        topic_model: A trained BERTopic instance
        doc (str): The document to analyze
        top_n (int): Number of top topics to show
        top_terms (int): Number of top terms to show per topic

    Example:
        >>> from my_topic_utils import show_top_topics_for_doc
        >>> show_top_topics_for_doc(topic_model, "This is my text", top_n=3)
    """
    # Get per-topic distribution (using c-TF-IDF approximation)
    dist, _ = topic_model.approximate_distribution(doc)

    # Flatten array (shape (1, n_topics) -> (n_topics,))
    dist = dist[0]

    # Get indices of top-N topics
    top_ids = np.argsort(dist)[::-1][:top_n]

    results = []
    for tid in top_ids:
        if dist[tid] > 0:  # skip empty contributions
            words = topic_model.get_topic(tid) or []
            terms = ", ".join([w for w, _ in words[:top_terms]])
            results.append((tid, dist[tid], terms))

    # Print nicely
    for tid, prob, terms in results:
        print(f"Topic {tid:>3} | {prob:.3f} | {terms}")

    return results  # in case you want to use programmatically



