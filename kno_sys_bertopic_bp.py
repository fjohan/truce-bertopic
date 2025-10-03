from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from my_topic_utils import get_topic_tree, show_top_topics_for_doc

# ---- Load TXT → documents (one doc per line) ----
txt_path = "kno_sys_AB_shuf.txt"
with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
    documents = [line.strip() for line in f if line.strip()]
print(f"{len(documents)} documents loaded from {txt_path}")

# ---- embeddings ----
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = sentence_model.encode(documents, show_progress_bar=True)

# Define sub-models
vectorizer = CountVectorizer(stop_words="english")
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
#hdbscan_model = HDBSCAN(min_cluster_size=20, min_samples=2, metric='euclidean', cluster_selection_method='eom')
hdbscan_model = HDBSCAN(min_cluster_size=80, min_samples=2, metric='euclidean', cluster_selection_method='eom')

# Train our topic model with BERTopic
topic_model = BERTopic(
    embedding_model=sentence_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer
).fit(documents, embeddings)
print(topic_model.get_topic_info())

# hierarchical topics
hierarchical_topics = topic_model.hierarchical_topics(documents)
html = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)
html.write_html("kno_sys_AB_hierarchy.html")

# tree groups
tree = get_topic_tree(hierarchical_topics, list_groups=True, indent_output=True)
print(tree)
tree = get_topic_tree(hierarchical_topics)
print(tree)

# datamap
html = topic_model.visualize_document_datamap(documents, embeddings=embeddings, interactive=True)
html.save("kno_sys_AB_docs_datamap.html")

# exmple doc to topic distribution
doc = "Farmers develop indigenous knowledge systems for agriculture."
show_top_topics_for_doc(topic_model, doc, top_n=5, top_terms=5)
