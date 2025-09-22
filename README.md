# Truce BERTopic Analysis

This repository explores hierarchical topic modeling of research abstracts related to **knowledge systems** using [BERTopic](https://maartengr.github.io/BERTopic/). It includes data, visualizations, and utility functions to explore and interpret topics.

---

## 🌍 Background

The project grew out of an interest in how the term *“knowledge system(s)”* is used across disciplines. By analyzing collections of abstracts and titles, the goal is to identify recurring themes (e.g., *indigenous knowledge systems*, *scientific knowledge systems*, *agricultural knowledge systems*) and understand how these themes cluster together or diverge.  

Using hierarchical topic modeling makes it possible to see both general groupings and more fine-grained topics, offering a structured view of how the notion of *knowledge systems* appears in scholarly writing.

---

## 📂 Repository Contents

| Type | Files | Purpose |
|------|-------|---------|
| **Data** | `kno_sys_AB_shuf.txt`, `kno_sys_TI_shuf.txt` | Raw text files containing research abstracts. |
| **Visualizations** | `kno_sys_AB_hierarchy.html`, `kno_sys_AB_docs_datamap.html` | Visualizations from BERTopic:  
| **Code** | Python and Bash scripts | Scripts for building BERTopic models, seeding topics, generating visualizations, and analyzing outputs. |
| **Utilities** | `my_topic_utils.py` | Helper functions for working with BERTopic topic trees and document–topic distributions. |

---

## 🧰 Utilities

- **`my_topic_utils.py`**  
  Custom helper functions:
  - `get_topic_tree(...)` — extract hierarchical topic trees as ASCII art or as ordered lists of aggregated label groups (general → specific).  
  - `show_top_topics_for_doc(...)` — given a document, print its top topic contributions with probabilities and representative terms.

- **HTML visualizations**  
  - **Hierarchy**: interactive view of topic merges, useful for exploring general vs. specific groupings.  
  - **Datamap**: shows each abstract as a point in embedding space, colored by topic, making relationships between documents more tangible.

---

## ✅ How to Interpret the Outputs

- **Hierarchical tree**  
  - The leftmost / top-level nodes correspond to the most general clusters.  
  - Nested nodes represent progressively more specific topics.  
  - Leaf nodes (`■── Topic: N`) are the original un-grouped topics accessible via `topic_model.get_topic(N)`.

- **Document-datamap**  
  - Each abstract is visualized in 2D based on its embeddings.  
  - Color indicates topic assignment.  
  - Clusters in the plot help reveal structural relations between documents.

- **Topic inspection for a document**  
  - A single abstract can be mapped to a distribution of topics.  
  - `show_top_topics_for_doc(...)` lists the most relevant topics, their weights, and their top representative terms.  
  - This is useful to see whether a document mixes multiple themes (e.g., *indigenous knowledge systems* vs. *scientific knowledge systems*).

---

## 💡 Notes and Possible Next Steps

- Seed domain-specific keywords (e.g., *indigenous, traditional, agricultural, scientific, western*) to guide topic formation more strongly.  
- Chunk long texts into smaller units (paragraphs/sentences) to allow multi-theme topic mixtures.  
- Export static images (PNG, SVG) from the HTML visualizations for reports or publications.  
- Explore stability of topics across different parameter choices (`min_topic_size`, embedding models).  

---

## 📄 License

Add your license information here (e.g. MIT, Apache 2.0).

---

## 🙋 Contact

For questions or suggestions, please open an issue in this repo.



