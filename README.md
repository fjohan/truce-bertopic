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
| **Visualizations** | `kno_sys_AB_hierarchy.html` | Visualizations from BERTopic:  
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

## 📊 Tentative Outcomes

From the current hierarchical topic model, two broad thematic clusters emerge:

---

### 1. Knowledge-based / formal systems
Covers computational, educational, managerial, and cultural/heritage aspects of “knowledge”.

- **Computational & logic models**  
  - Logic, queries, semantics (Topic 3)  
  - Materials/microstructure frameworks (Topic 15)  
- **Applied knowledge in organizations and design**  
  - Decision support and expert systems (Topic 16)  
  - Knowledge/data/ontology for domains (Topic 7, Topic 8)  
  - Knowledge management & innovation (Topic 2)  
  - Product design & manufacturing processes (Topic 11)  
- **Teaching and learning**  
  - Pedagogy, students, courses (Topic 1)  
- **Memory, culture, and heritage**  
  - Cultural heritage and digitization (Topic 17)  
  - Science, wisdom, social knowledge (Topic 18)  
  - Cognitive/brain/visual aspects (Topic 13)

---

### 2. Indigenous and local knowledge systems
Focuses on *knowledge systems embedded in local, ecological, and cultural contexts*.

- **Climate change and adaptation**  
  - Farmers and weather knowledge (Topic 20)  
  - Indigenous adaptation and peoples (Topic 19)  
  - Disaster risk and floods (Topic 14)  
- **Health, education, and sustainability**  
  - Indigenous knowledge in education and health (Topic 0)  
  - Links to sustainability and science (Topic 12)  
- **Conservation and ecology**  
  - Biodiversity and ecosystems (Topic 5)  
  - Fisheries and coastal/marine management (Topic 9)  
- **Agriculture and food systems**  
  - Forest and traditional practices (Topic 10)  
  - Farmers, food, agriculture (Topic 6)  
- **Medicinal plants**  
  - Traditional species and plant knowledge (Topic 4)

---

**Takeaway:**  
The notion of *knowledge systems* in the corpus splits into two overarching uses:  
(1) as **formalized, technical frameworks** (models, ontologies, education, heritage), and  
(2) as **embedded, community-based practices** (indigenous, agricultural, ecological, medicinal).

---

## 💡 Notes and Possible Next Steps

- Seed domain-specific keywords (e.g., *indigenous, traditional, agricultural, scientific, western*) to guide topic formation more strongly.  
- Chunk long texts into smaller units (paragraphs/sentences) to allow multi-theme topic mixtures.  
- Export static images (PNG, SVG) from the HTML visualizations for reports or publications.  
- Explore stability of topics across different parameter choices (`min_topic_size`, embedding models).  

