"""Generate a LinkedIn-style profile PDF (same layout as Ed's me/linkedin.pdf).

Edit the PROFILE dict below, then regenerate with:
    uv run --with fpdf2 python generate_linkedin_pdf.py

Anything in [brackets] is a placeholder — replace it with your real details.
"""

from fpdf import FPDF

PROFILE = {
    "name": "Mingwei Sun",
    "headline": "Senior Data Scientist at Constellation",
    "location": "New York, New York, United States",
    "contact": [
        "mingwei.sun@constellationagency.com",
        "www.linkedin.com/in/mingwei-sun-876992156 (LinkedIn)",
    ],
    "top_skills": [
        "Machine Learning",
        "Multi-Agent Systems & RAG",
        "MLOps",
    ],
    "certifications": [
        "Claude Code: A Highly Agentic Coding Assistant (DeepLearning.AI, May 2026)",
        "Supervised Machine Learning: Regression and Classification (Coursera)",
    ],
    "summary": (
        "I'm a Senior Data Scientist at Constellation in New York, where I build "
        "data-driven solutions for the advertising and marketing technology "
        "industry. My expertise spans multi-agent systems, Retrieval-Augmented "
        "Generation (RAG), and MLOps, on a foundation of statistical analysis, "
        "machine learning, and data visualization. Before moving into ad tech, "
        "I worked in healthcare data science at Boston Children's Hospital, "
        "supporting clinical research with statistical modeling. "
        "[Add a personal line - what you enjoy, hobbies, what you're exploring.]"
    ),
    "experience": [
        {
            "company": "Constellation",
            "title": "Senior Data Scientist",
            "dates": "[Month 20XX] - Present",
            "location": "New York, New York, United States",
            "description": (
                "Data science for digital advertising and marketing technology: "
                "building ML models and data-driven insights for automotive and "
                "other verticals. Recent work includes multi-agent systems, RAG "
                "pipelines, and MLOps. [Add specifics: projects, stack, impact.]"
            ),
        },
        {
            "company": "Boston Children's Hospital",
            "title": "Data Scientist / Biostatistician",
            "dates": "[Month 20XX] - [Month 20XX]",
            "location": "Boston, Massachusetts, United States",
            "description": (
                "Applied statistical methodologies to support clinical research "
                "and healthcare initiatives. [Add specifics of your projects.]"
            ),
        },
        {
            "company": "72 Dragons",
            "title": "Data Analyst",
            "dates": "[Month 20XX] - [Month 20XX]",
            "location": "[City, Country]",
            "description": (
                "Data analysis and interpretation. [Add specifics of your work.]"
            ),
        },
        {
            "company": "Hisense TransTech",
            "title": "Algorithm Developer Intern",
            "dates": "[Month 20XX] - [Month 20XX]",
            "location": "[Qingdao, China]",
            "description": (
                "Algorithm design and data preprocessing. [Add specifics.]"
            ),
        },
    ],
    "education": [
        {
            "school": "Columbia University in the City of New York",
            "detail": "Master of Arts, [Field of Study] - (2017 - 2018)",
        },
        {
            "school": "China University of Geosciences (Beijing)",
            "detail": "Bachelor's degree, [Field of Study] - (2012 - 2016)",
        },
    ],
}

# ---- layout ----------------------------------------------------------------

PAGE_W, PAGE_H = 215.9, 279.4  # US Letter, mm
SIDEBAR_W = 62
MAIN_X = SIDEBAR_W + 12
RIGHT_MARGIN = 15
DARK = (40, 62, 74)
GRAY = (110, 110, 110)
LIGHT = (235, 238, 240)


class LinkedInPDF(FPDF):
    def header(self):
        self.set_fill_color(*DARK)
        self.rect(0, 0, SIDEBAR_W, PAGE_H, style="F")

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()} of {{nb}}", align="C")

    def section_heading(self, text):
        self.ln(6)
        self.set_font("helvetica", "", 16)
        self.set_text_color(30, 30, 30)
        self.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text, size=10):
        self.set_font("helvetica", "", size)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")


def draw_sidebar(pdf):
    x, w = 8, SIDEBAR_W - 14
    pdf.set_xy(x, 20)
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(*LIGHT)
    pdf.cell(w, 6, "Contact", new_x="LEFT", new_y="NEXT")
    pdf.set_font("helvetica", "", 8.5)
    for line in PROFILE["contact"]:
        pdf.set_x(x)
        pdf.multi_cell(w, 4.5, line)
        pdf.ln(1)

    pdf.ln(6)
    pdf.set_x(x)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(w, 6, "Top Skills", new_x="LEFT", new_y="NEXT")
    pdf.set_font("helvetica", "", 9)
    for skill in PROFILE["top_skills"]:
        pdf.set_x(x)
        pdf.multi_cell(w, 5, skill)

    pdf.ln(6)
    pdf.set_x(x)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(w, 6, "Certifications", new_x="LEFT", new_y="NEXT")
    pdf.set_font("helvetica", "", 8.5)
    for cert in PROFILE.get("certifications", []):
        pdf.set_x(x)
        pdf.multi_cell(w, 4.5, cert)
        pdf.ln(1)


def build():
    pdf = LinkedInPDF(unit="mm", format="letter")
    pdf.set_auto_page_break(True, margin=20)
    pdf.set_margins(MAIN_X, 15, RIGHT_MARGIN)
    pdf.add_page()
    draw_sidebar(pdf)

    pdf.set_xy(MAIN_X, 18)
    pdf.set_font("helvetica", "", 24)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 11, PROFILE["name"], new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 5.5, PROFILE["headline"], new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5, PROFILE["location"], new_x="LMARGIN", new_y="NEXT")

    pdf.section_heading("Summary")
    pdf.body_text(PROFILE["summary"])

    pdf.section_heading("Experience")
    for job in PROFILE["experience"]:
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5.5, job["company"], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10.5)
        pdf.multi_cell(0, 5, job["title"], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(*GRAY)
        pdf.multi_cell(0, 4.5, f"{job['dates']}", new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(0, 4.5, job["location"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.5)
        pdf.body_text(job["description"])
        pdf.ln(4)

    pdf.section_heading("Education")
    for edu in PROFILE["education"]:
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5.5, edu["school"], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(*GRAY)
        pdf.multi_cell(0, 5, edu["detail"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    out = "linkedin_mingwei.pdf"
    pdf.output(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    build()
