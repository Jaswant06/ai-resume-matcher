"""Gradio web app for the AI Resume Matcher.

Paste a resume and a job description to get an overall match score, the
requirements you already cover, and the gaps to address before applying.
"""

import gradio as gr

from src import analyze, format_report

EXAMPLE_RESUME = """Experienced Python developer with 3 years building machine learning models.
Strong background in deep learning with PyTorch and TensorFlow.
Built and fine-tuned NLP models including transformers for text classification.
Deployed models to production as REST APIs serving real users.
Comfortable with data analysis using pandas and scikit-learn."""

EXAMPLE_JOB = """We are hiring a Machine Learning Engineer.
Strong Python programming skills are required.
Experience with deep learning frameworks such as PyTorch or TensorFlow.
Must have experience deploying models to production as APIs.
Familiarity with AWS cloud and Docker containers is a strong plus.
Experience with SQL and data pipelines preferred."""


def run(resume_text: str, job_text: str) -> str:
    if not resume_text.strip() or not job_text.strip():
        return "Please paste **both** your resume and a job description above."
    return format_report(analyze(resume_text, job_text))


THEME = gr.themes.Soft(
    primary_hue="teal",
    secondary_hue="indigo",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
    radius_size=gr.themes.sizes.radius_lg,
)

CSS = """
#wrap { max-width: 940px; margin: 0 auto; padding-bottom: 28px; }
#hero { margin: 8px 0 20px; }
#card {
  background: var(--background-fill-primary);
  border-radius: 18px; padding: 20px 20px 10px;
  box-shadow: 0 12px 34px rgba(2, 6, 23, 0.07);
  border: 1px solid rgba(2, 6, 23, 0.05);
}
#analyze-btn {
  background: linear-gradient(135deg, #0d9488 0%, #4f46e5 100%) !important;
  border: none !important; color: #fff !important; font-weight: 600 !important;
  box-shadow: 0 8px 22px rgba(79, 70, 229, 0.28) !important;
  transition: transform .15s ease, box-shadow .15s ease !important;
}
#analyze-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 14px 32px rgba(79, 70, 229, 0.40) !important;
}
#result { margin-top: 16px; }
footer { display: none !important; }
"""

HERO = """
<div style="background: linear-gradient(135deg,#0f766e 0%,#0e7490 45%,#4338ca 100%);
            border-radius: 22px; padding: 48px 28px; text-align: center; color: #ffffff;
            box-shadow: 0 18px 50px rgba(67,56,202,0.28);">
  <div style="display:inline-block; padding:5px 14px; border-radius:999px; font-size:.8rem;
              letter-spacing:.08em; text-transform:uppercase; background:rgba(255,255,255,.16);
              margin-bottom:16px;">Semantic AI</div>
  <div style="font-size: 2.8rem; font-weight: 800; letter-spacing: -0.02em; line-height:1.08;">
    Resume&nbsp;Matcher
  </div>
  <div style="font-size: 1.1rem; opacity: .92; margin: 16px auto 0; max-width: 600px; line-height:1.55;">
    Instantly see how well your resume fits any role, and exactly what to add
    before you apply. Meaning-based matching, not keyword guessing.
  </div>
</div>
"""


def build_ui() -> gr.Blocks:
    with gr.Blocks(theme=THEME, css=CSS, title="AI Resume Matcher") as demo:
        with gr.Column(elem_id="wrap"):
            gr.HTML(HERO, elem_id="hero")
            with gr.Column(elem_id="card"):
                with gr.Row(equal_height=True):
                    resume_in = gr.Textbox(
                        label="Your resume", lines=15,
                        placeholder="Paste your resume here...",
                    )
                    job_in = gr.Textbox(
                        label="Job description", lines=15,
                        placeholder="Paste the job posting here...",
                    )
                analyze_btn = gr.Button(
                    "Analyze match", variant="primary",
                    size="lg", elem_id="analyze-btn",
                )
            output = gr.Markdown(elem_id="result")

            with gr.Accordion("How it works", open=False):
                gr.Markdown(
                    "Both texts are turned into sentence embeddings (vectors that "
                    "capture meaning). Each requirement in the job description is "
                    "matched against the most similar line in your resume, so it "
                    "compares meaning rather than exact keywords. Scores are "
                    "relative: look at the gaps, not the absolute percentage."
                )

            analyze_btn.click(run, inputs=[resume_in, job_in], outputs=output)
            gr.Examples(
                examples=[[EXAMPLE_RESUME, EXAMPLE_JOB]],
                inputs=[resume_in, job_in],
                label="Try an example",
            )
    return demo


if __name__ == "__main__":
    build_ui().launch()
