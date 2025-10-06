# bertopic_runner.py
# Usage:
#   python bertopic_runner.py --input bio_los.txt --min-cluster-size 20
#   python bertopic_runner.py -i kno_sys.txt -m 30

import argparse
from pathlib import Path
import pandas as pd

from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer

# If you have your utilities in a separate file:
from my_topic_utils import get_topic_tree  # optional, used for printing tree groups

def main():
    parser = argparse.ArgumentParser(description="BERTopic over title/abstract TSV.")
    parser.add_argument("-i", "--input", required=True, help="Path to TSV with: title<TAB>abstract")
    parser.add_argument("-m", "--min-cluster-size", type=int, default=20,
                        help="HDBSCAN min_cluster_size (default: 20)")
    parser.add_argument("--has-header", action="store_true",
                        help="Set if the TSV has a header row (default assumes no header).")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise FileNotFoundError(f"Input not found: {in_path}")

    base = in_path.stem
    mcs = args.min_cluster_size

    # ---------- Load title/abstract TSV ----------
    header = 0 if not args.has_header else "infer"
    df = pd.read_csv(
        in_path,
        sep="\t",
        header=header,
        names=["title", "abstract"] if header == 0 else None,
        dtype=str,
        on_bad_lines="skip",
        encoding="utf-8",
    )
    df = df.dropna(subset=["title", "abstract"])
    df["title"] = df["title"].str.strip()
    df["abstract"] = df["abstract"].str.strip()

    titles = df["title"].tolist()
    abstracts = df["abstract"].tolist()
    assert len(titles) == len(abstracts) and len(abstracts) > 0, f"No valid rows found in {in_path}"
    print(f"{len(abstracts)} rows loaded from {in_path}")

    # ---------- Embeddings from ABSTRACTS ----------
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = sentence_model.encode(abstracts, show_progress_bar=True)

    # ---------- Sub-models ----------
    vectorizer = CountVectorizer(stop_words="english")
    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
    hdbscan_model = HDBSCAN(
        min_cluster_size=mcs,
        min_samples=2,
        metric='euclidean',
        cluster_selection_method='eom'
    )

    # ---------- Fit BERTopic on ABSTRACTS ----------
    topic_model = BERTopic(
        embedding_model=sentence_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer
    ).fit(abstracts, embeddings)

    print(topic_model.get_topic_info())

    # ---------- Hierarchical topics ----------
    hierarchical_topics = topic_model.hierarchical_topics(abstracts)
    fig_h = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)

    out_h = f"{base}_hierarchy_{mcs}.html"
    fig_h.write_html(out_h)

    # Optional: grouped labels using your custom tree helper
    try:
        tree_groups = get_topic_tree(hierarchical_topics, list_groups=True, indent_output=True)
        print(tree_groups)
    except Exception as e:
        print(f"(Optional) get_topic_tree failed: {e}")

    # ---------- Datamap with TITLES as labels ----------
    # NOTE: use 'documents=' not 'docs='
    datamap = topic_model.visualize_document_datamap(
        docs=titles,         # hover labels = titles
        embeddings=embeddings,
        interactive=True
    )
    out_d = f"{base}_datamap_{mcs}.html"
    datamap.save(out_d)

    print(f"Saved: {out_h} and {out_d}")

if __name__ == "__main__":
    main()


