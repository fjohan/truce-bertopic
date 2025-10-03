# pip install bertopic sentence-transformers umap-learn hdbscan scikit-learn pandas plotly kaleido

from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from my_topic_utils import get_topic_tree, show_top_topics_for_doc
import pandas as pd


# cat savedrecs* > kno_sys_all.txt
# awk -F'\t' '{if ($9 != "" && $22 != "") print $9"\t"$22}' kno_sys_all.txt | sort | uniq | grep -v '^TI.*AB$' > TI_AB.txt ; shuf TI_AB.txt > TI_AB_shuf.txt

# ---------- Load title/abstract TSV ----------
# Assumes tab-separated with two columns: Title \t Abstract
# If your file has a header line, set HAS_HEADER = None; otherwise 0.
HAS_HEADER = 0  # auto-detect header if present; set to 0 if there is no header
df = pd.read_csv(
    "TI_AB_shuf.txt",
    sep="\t",
    header=HAS_HEADER,
    names=["title", "abstract"] if HAS_HEADER == 0 else None,
    dtype=str,
    on_bad_lines="skip",
    encoding="utf-8",
)

# Clean up & basic sanity checks
df = df.dropna(subset=["title", "abstract"])
df["title"] = df["title"].str.strip()
df["abstract"] = df["abstract"].str.strip()
titles = df["title"].tolist()
abstracts = df["abstract"].tolist()
assert len(titles) == len(abstracts) and len(abstracts) > 0, "No rows found in TI_AB.txt"
print(f"{len(abstracts)} rows loaded from TI_AB.txt")

# ---------- Embeddings from ABSTRACTS ----------
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = sentence_model.encode(abstracts, show_progress_bar=True)

# ---------- Sub-models (your settings) ----------
vectorizer = CountVectorizer(stop_words="english")
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
# Choose one:
hdbscan_model = HDBSCAN(min_cluster_size=80, min_samples=2, metric='euclidean', cluster_selection_method='eom')
#hdbscan_model = HDBSCAN(min_cluster_size=80, min_samples=2, metric='euclidean', cluster_selection_method='eom')

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
fig_h.write_html("TI_AB_hierarchy_aqures.html")

# Optional: grouped labels from your custom tree printer
tree_groups = get_topic_tree(hierarchical_topics, list_groups=True, indent_output=True)
print(tree_groups)
tree = get_topic_tree(hierarchical_topics)
print(tree)

# ---------- Datamap with TITLES as labels ----------
# IMPORTANT: pass titles as `documents` (used for hover labels),
# but embeddings come from ABSTRACTS.
datamap = topic_model.visualize_document_datamap(
    docs=titles,            # labels/hover
    embeddings=embeddings,
    interactive=True
)
datamap.save("TI_AB_titles_datamap_aqures.html")

print("Saved: TI_AB_hierarchy.html and TI_AB_titles_datamap.html")


