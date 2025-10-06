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
| **Visualizations** | `TI_AB_hierarchy.html`, `TI_AB_titles_datamap.html` | Visualization from BERTopic  
| **Code** | Python and Bash scripts | Scripts for building BERTopic models, seeding topics, generating visualizations, and analyzing outputs. |
| **Utilities** | `my_topic_utils.py` | Helper functions for working with BERTopic topic trees and document–topic distributions. |

---

## 🧰 Utilities

- **`my_topic_utils.py`**  
  Custom helper functions:
  - `get_topic_tree(...)` — extract hierarchical topic trees as ASCII art or as ordered lists of aggregated label groups (general → specific).  
  - `show_top_topics_for_doc(...)` — given a document, print its top topic contributions with probabilities and representative terms.

- **HTML visualizations**  
  - **Hierarchy**: interactive view of topic merges, useful for exploring general vs. specific groupings. [Link](https://fjohan.github.io/truce-bertopic/TI_AB_hierarchy.html)
  - **Datamap**: shows each abstract as a point in embedding space, colored by topic, making relationships between documents more tangible. [Link](https://fjohan.github.io/truce-bertopic/TI_AB_titles_datamap.html)
  - [Link](https://fjohan.github.io/truce-bertopic/bio_los_hierarchy_32.html)
  - [Link](https://fjohan.github.io/truce-bertopic/bio_los_datamap_32.html)
  - [Link](https://fjohan.github.io/truce-bertopic/lyrics_docs_datamap_custom_labels.html)
  - [Link](https://fjohan.github.io/truce-bertopic/lyrics_docs_datamap_by_artist.html)

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

## 📊 Tentative Outcomes (updated)

From the current hierarchical topic model, two broad thematic clusters emerge:

---

### 1. Indigenous and local knowledge systems  
Emphasizes practice-based, ecological, and community contexts.

- **Medicinal plants**  
  - Traditional plant/medicine knowledge (Topic 10)

- **Education, sustainability, and policy**  
  - Ecosystem services, biodiversity values, IPBES (Topic 16)  
  - Sustainability, climate, adaptation policies (Topic 6)  
  - Indigenous peoples’ climate knowledge (Topic 3)  
  - Indigenous knowledge in education/research systems (Topic 0)

- **Local resource management & agriculture**  
  - Fisheries, coastal & marine knowledge (Topic 7)  
  - Species/biodiversity conservation (Topic 13)  
  - Forests & indigenous conservation practices (Topic 9)  
  - Farmers, soil, and food systems (Topic 2)

- **Climate change & risk**  
  - Farmers’ weather and adaptation knowledge (Topic 5)  
  - Disaster risk and floods (Topic 15)

---

### 2. Knowledge systems as formal/technical models  
Covers comparative traditions, cognitive/semantic systems, and applied models.

- **Comparative knowledge traditions**  
  - Chinese/Western medical systems (Topic 17)  
  - Indian/Sanskrit/colonial education traditions (Topic 19)

- **Cognition, science, and digital knowledge**  
  - Memory, brain, semantic knowledge (Topic 12)  
  - Science as human/social knowledge (Topic 8)  
  - AI, open science, digital knowledge infrastructures (Topic 18)

- **Applied models & design**  
  - Medical/TCM disease knowledge (Topic 14)  
  - Innovation, management & performance (Topic 4)  
  - Model/design systems (Topic 1)  
  - Teaching, learning, students & education (Topic 11)

- **Engineering frameworks**  
  - Materials microstructure & MKS frameworks (Topic 20)

---

### 🔑 Takeaway
The notion of *knowledge systems* in the corpus splits into two overarching uses:

1. **Embedded/local practices** — indigenous knowledge, agriculture, fisheries, biodiversity, adaptation, and traditional medicine.  
2. **Formalized systems** — scientific models, cognitive/semantic frameworks, AI/digital knowledge, cross-cultural knowledge traditions, and organizational/educational models.  

Delving deeper:  
- The *indigenous/local* side shows sub-themes (policy/IPBES, disaster risk, agriculture).  
- The *formal/technical* side surfaces cross-cultural comparisons (Chinese/Western, Indian/colonial) alongside technical knowledge models.

---

## 💡 Notes and Possible Next Steps

- Seed domain-specific keywords (e.g., *indigenous, traditional, agricultural, scientific, western*) to guide topic formation more strongly.  
- Chunk long texts into smaller units (paragraphs/sentences) to allow multi-theme topic mixtures.  
- Export static images (PNG, SVG) from the HTML visualizations for reports or publications.  
- Explore stability of topics across different parameter choices (`min_topic_size`, embedding models).  

