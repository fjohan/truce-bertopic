from bertopic import BERTopic
import pandas as pd

from bertopic.representation import KeyBERTInspired

from sentence_transformers import SentenceTransformer
#from umap import UMAP

# Load the data
file_path = 'reindeer_climate_forag_ecology_abstract.xls'
#file_path = 'savedrecs.xls'
df = pd.read_excel(file_path)
#df = pd.read_csv('snow.csv')


# Preprocess the data (ensure there are no NaN values in the Abstract column)
documents = df['Abstract'].dropna().tolist()
df['Abstract'].dropna().to_csv('rcfe.csv')

# use this for Eira_2012
#df = pd.read_csv('Eira_2012_4_4.txt', sep="\t",header=None)
#documents = df[0].dropna().tolist()

representation_model = KeyBERTInspired()
#topic_model = BERTopic(representation_model=representation_model,min_topic_size=2) # set low for 50 documents
#topics, probabilities = topic_model.fit_transform(documents)
#topic_model.get_topic_info()

sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
#embeddings = sentence_model.encode(documents, show_progress_bar=True)

#topic_model.visualize_documents(documents, embeddings=embeddings)

#topic_model.visualize_barchart()

#topic_model.visualize_heatmap()

# sentence level
from nltk.tokenize import sent_tokenize, word_tokenize
sentences = [sent_tokenize(abstract) for abstract in documents]
sentences = [sentence for doc in sentences for sentence in doc]

mts=3
topic_model = BERTopic(representation_model=representation_model,min_topic_size=mts)
topics, probabilities = topic_model.fit_transform(sentences)
#topic_model.get_topic_info()

#topic_model.visualize_topics()

#hierarchical_topics = topic_model.hierarchical_topics(sentences)
#topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)

#tree = topic_model.get_topic_tree(hierarchical_topics)
#print(tree)

#vis = topic_model.visualize_barchart()
#vis.write_html('barchart.html')

embeddings = sentence_model.encode(sentences, show_progress_bar=True)
html = topic_model.visualize_document_datamap(sentences, embeddings=embeddings, interactive=True)
#html.save('eira_2012_4_4_map.html')
html.save('rcfe.html')

