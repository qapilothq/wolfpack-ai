import os

ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
OPENAI_FAST_MODEL = os.getenv('OPENAI_FAST_MODEL')
DEFAULT_MAX_TOKENS = int(os.getenv('DEFAULT_MAX_TOKENS'))
GPT_4O_CONTEXT_WINDOW = int(os.getenv('GPT_4O_CONTEXT_WINDOW'))

# Define font presets
FONT_PRESETS = {
    'sans-serif': "Helvetica, Helvetica-Bold, Helvetica-Oblique, Helvetica-BoldOblique, sans-serif",
    'serif': "Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic, serif",
    'mono': "Courier, Courier-Bold, Courier-Oblique, Courier-BoldOblique, monospace"
}

EMPHASIS = {
    "technical_skills_weight": 40,
    "soft_skills_weight": 15,
    "experience_weight": 10,
    "education_weight": 5,
    "language_proficiency_weight": 15,
    "certifications_weight": 5,
    "location_weight": 10
}