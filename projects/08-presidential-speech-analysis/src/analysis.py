"""Transparent lexical, readability, similarity, and exploratory topic analysis."""

from __future__ import annotations

import collections
import json
import os
import re
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "portfolio-matplotlib-cache"))
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, write_json

TOKEN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _syllables(word: str) -> int:
    groups = re.findall(r"[aeiouy]+", word.lower())
    count = len(groups)
    if word.lower().endswith("e") and count > 1: count -= 1
    return max(1, count)


def _document_metrics(text: str) -> dict[str, object]:
    words = TOKEN.findall(text.lower()); content = [word for word in words if word not in ENGLISH_STOP_WORDS and len(word) > 2]
    sentences = [sentence for sentence in SENTENCE.split(text.strip()) if TOKEN.search(sentence)]
    syllables = sum(_syllables(word) for word in words)
    reading_ease = 206.835 - 1.015 * (len(words) / max(1, len(sentences))) - 84.6 * (syllables / max(1, len(words)))
    return {"words": len(words), "sentences": len(sentences), "unique_words": len(set(words)), "unique_content_words": len(set(content)), "lexical_diversity": len(set(words)) / len(words), "average_sentence_words": len(words) / max(1, len(sentences)), "flesch_reading_ease_approximate": reading_ease, "top_content_words": dict(collections.Counter(content).most_common(15))}


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    files = {"Roosevelt 1941": "roosevelt_1941.xlsx", "Kennedy 1961": "kennedy_1961.xlsx", "Nixon 1973": "nixon_1973.xlsx"}
    documents = {}; quality_frames = []
    for label, filename in files.items():
        frame = pd.read_excel(ROOT / "data" / filename); quality = data_quality_table(frame); quality.insert(0, "document", label); quality_frames.append(quality)
        documents[label] = str(frame.loc[0, "Speech"]).replace("\\n", " ").replace("\\t", " ")
    pd.concat(quality_frames, ignore_index=True).to_csv(paths["tables"] / "data_quality.csv", index=False)
    metrics = {label: _document_metrics(text) for label, text in documents.items()}
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    matrix = vectorizer.fit_transform(documents.values()); similarity = cosine_similarity(matrix)
    labels = list(documents)
    similarity_table = pd.DataFrame(similarity, index=labels, columns=labels)
    terms = np.asarray(vectorizer.get_feature_names_out())
    distinctive_rows = []
    for index, label in enumerate(labels):
        for position in matrix[index].toarray().ravel().argsort()[-15:][::-1]:
            distinctive_rows.append({"document": label, "term": terms[position], "tfidf": float(matrix[index, position])})
    distinctive = pd.DataFrame(distinctive_rows)

    sentence_rows = []
    for label, text in documents.items():
        for sentence in SENTENCE.split(text.strip()):
            if len(TOKEN.findall(sentence)) >= 5: sentence_rows.append({"document": label, "sentence": sentence})
    sentences = pd.DataFrame(sentence_rows)
    sentence_vectorizer = TfidfVectorizer(stop_words="english", min_df=2, max_df=0.85, ngram_range=(1, 2), max_features=1200)
    sentence_matrix = sentence_vectorizer.fit_transform(sentences["sentence"])
    topic_model = NMF(n_components=3, init="nndsvda", random_state=42, max_iter=500).fit(sentence_matrix)
    topic_terms = np.asarray(sentence_vectorizer.get_feature_names_out())
    topic_rows = []
    for topic, weights in enumerate(topic_model.components_):
        topic_rows.append({"topic": topic + 1, "top_terms": ", ".join(topic_terms[weights.argsort()[-10:][::-1]])})
    sentence_topics = topic_model.transform(sentence_matrix)
    sentences["dominant_topic"] = sentence_topics.argmax(axis=1) + 1
    topic_share = pd.crosstab(sentences["document"], sentences["dominant_topic"], normalize="index")
    metric_table = pd.DataFrame(metrics).T.drop(columns="top_content_words")
    metric_table.to_csv(paths["tables"] / "corpus_metrics.csv"); similarity_table.to_csv(paths["tables"] / "tfidf_similarity.csv")
    distinctive.to_csv(paths["tables"] / "distinctive_tfidf_terms.csv", index=False); pd.DataFrame(topic_rows).to_csv(paths["tables"] / "exploratory_topics.csv", index=False); topic_share.to_csv(paths["tables"] / "topic_share_by_speech.csv")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    for label in labels:
        top = pd.Series(metrics[label]["top_content_words"]).head(10).sort_values()
        axes[0, 0].plot(top.values, top.index, marker="o", label=label)
    axes[0, 0].set(title="Most frequent content words", xlabel="Count"); axes[0, 0].legend(fontsize=8)
    image = axes[0, 1].imshow(similarity_table, cmap="Blues", vmin=0, vmax=1)
    axes[0, 1].set(title="TF-IDF cosine similarity", xticks=range(3), xticklabels=labels, yticks=range(3), yticklabels=labels)
    for (row, col), value in np.ndenumerate(similarity): axes[0, 1].text(col, row, f"{value:.2f}", ha="center", va="center")
    fig.colorbar(image, ax=axes[0, 1], fraction=0.046)
    metric_table[["lexical_diversity", "flesch_reading_ease_approximate"]].plot.bar(ax=axes[1, 0], secondary_y="flesch_reading_ease_approximate", color=["#2f6690", "#e9a03b"])
    axes[1, 0].set(title="Lexical diversity and approximate readability", xlabel="Speech"); axes[1, 0].tick_params(axis="x", rotation=25)
    topic_share.plot.bar(stacked=True, ax=axes[1, 1], colormap="viridis"); axes[1, 1].set(title="Exploratory sentence-topic composition", xlabel="Speech", ylabel="Share of sentences"); axes[1, 1].tick_params(axis="x", rotation=25)
    fig.tight_layout(); fig.savefig(paths["figures"] / "speech_analysis_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    pair_rows = []
    for row in range(len(labels)):
        for col in range(row + 1, len(labels)): pair_rows.append({"pair": f"{labels[row]} vs {labels[col]}", "cosine_similarity": float(similarity[row, col])})
    results = {
        "status": "passed", "documents": metrics,
        "tfidf_similarity_pairs": sorted(pair_rows, key=lambda item: item["cosine_similarity"], reverse=True),
        "distinctive_terms": distinctive.groupby("document").apply(lambda frame: frame[["term", "tfidf"]].to_dict(orient="records"), include_groups=False).to_dict(),
        "exploratory_topics": topic_rows, "topic_share_by_speech": topic_share.round(4).to_dict(orient="index"),
        "method_note": "Readability uses an approximate syllable heuristic. NMF topics are exploratory patterns in three speeches, not objective historical themes or evidence of intent.",
        "responsible_use": "Lexical counts, similarity, readability, and topics do not establish ideology, truthfulness, policy effect, or speaker intent.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
