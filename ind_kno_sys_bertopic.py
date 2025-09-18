# pip install bertopic sentence-transformers
import pandas as pd

# ---------------------------
# Topic modeling (pick a variant)
# ---------------------------
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from sentence_transformers import SentenceTransformer

file_path = 'ind_kno_sys.xls'
df = pd.read_excel(file_path)
documents = df['Abstract'].dropna().tolist()

representation_model = KeyBERTInspired()
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = sentence_model.encode(documents, show_progress_bar=True)

mts = 5 # smaller - more topics
topic_model = BERTopic(representation_model=representation_model, min_topic_size=mts)

topics, probabilities = topic_model.fit_transform(documents)
topic_model.get_topic_info()

hierarchical_topics = topic_model.hierarchical_topics(documents)
tree = topic_model.get_topic_tree(hierarchical_topics)
print(tree)

html = topic_model.visualize_document_datamap(documents, embeddings=embeddings, interactive=True)
html.save("ind_kno_sys_mts5.html")


