# AI Resume Matcher: Semantic Resume & Job Description Matching (NLP / Embeddings)

An **AI resume matcher** that compares your resume against a job description using
**sentence embeddings and semantic search**, not keyword matching. It scores how
well you fit a role and tells you which requirements your resume doesn't yet cover,
so you know what to fix before applying.

> Paste a resume + a job posting -> get a **match score** and a **skill-gap list**.

## Why semantic matching (and not keywords)

Keyword matching misses meaning. "Built NLP models" and "experience with natural
language processing" share almost no words but mean the same thing. This tool
converts both texts into **embeddings** (vectors where similar meaning lands close
together), so it matches on *meaning*. Example: two sentences that share only one
word can still score 0.84 similarity.

## How it works

1. **Chunk:** the job description is split into individual requirements; the resume
   into lines. Requirements are extracted from the text itself (nothing hard-coded).
2. **Embed:** every chunk is turned into a 384-dimension vector with
   `all-MiniLM-L6-v2` (Sentence-Transformers).
3. **Match:** each job requirement is compared against every resume chunk via
   cosine similarity; the best-matching resume line is its coverage score.
4. **Report:** an overall match score, the covered requirements (with the resume
   line that matched each), and the gaps to address.

## Tech stack

Python · Sentence-Transformers · Hugging Face · PyTorch · Gradio · cosine similarity

## Run it locally

```bash
pip install -r requirements.txt
python app.py            # launches the web UI at http://127.0.0.1:7860
```

Run the tests:

```bash
pip install pytest
pytest
```

## Project structure

```text
ai-resume-matcher/
├── app.py                  # Gradio web UI (entry point)
├── src/
│   ├── __init__.py         # public API: analyze, format_report
│   ├── matcher.py          # core engine: chunk -> embed -> match -> score
│   └── report.py           # renders results as a Markdown report
├── tests/
│   └── test_matcher.py     # unit tests for the engine
├── requirements.txt
├── .gitignore
└── README.md
```

## Limitations

- **Scores are relative, not absolute.** There's no universal "good match" number;
  use the *gap* between covered and missing requirements, not the raw percentage.
- **Best-match (max) pooling can inflate near-misses.** A requirement that is merely
  *adjacent* in meaning to a resume line (e.g. "AWS" vs "deployed to production") can
  creep up toward the threshold. The covered/gap cutoff (default 0.30) is tunable.
- **Noisy job text** (boilerplate like benefits or EEO statements) is treated as a
  requirement and may show as a low-scoring "gap." A short-line filter removes the
  worst of it, but this is heuristic.
- **Semantic similarity is not logical reasoning.** The tool measures whether a
  requirement is *present and similar* in the resume, not whether it is *satisfied*.
  It cannot infer that "5 years" meets a "3+ years" requirement, or that a "B.Com. in
  Management" satisfies a "Business degree" requirement, and a skill buried in a long
  comma-separated list gets diluted. Reasoning about equivalence and thresholds needs
  a large language model, which is planned for a future version.

## Possible next steps

- **LLM-based v2:** use a language model to extract structured requirements and reason
  about coverage (years of experience, degree equivalence, skills in lists).
- Auto-extract real *skills* (not whole sentences) from the job posting.
- PDF resume upload.
- Tunable threshold in the UI.

---

Keywords: ai resume matcher, resume job matcher, semantic search, sentence
embeddings, NLP, resume screening, skill gap analysis, Sentence-Transformers,
Hugging Face, cosine similarity.
