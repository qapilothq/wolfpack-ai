import os

ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20240620')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
OPENAI_FAST_MODEL = os.getenv('OPENAI_FAST_MODEL', 'gpt-4o-mini-2024-07-18')
DEFAULT_MAX_TOKENS = int(os.getenv('DEFAULT_MAX_TOKENS', '1000'))
GPT_4O_CONTEXT_WINDOW = int(os.getenv('GPT_4O_CONTEXT_WINDOW', '128000'))

# Define font presets
FONT_PRESETS = {
    'sans-serif': "Helvetica, Helvetica-Bold, Helvetica-Oblique, Helvetica-BoldOblique, sans-serif",
    'serif': "Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic, serif",
    'mono': "Courier, Courier-Bold, Courier-Oblique, Courier-BoldOblique, monospace"
}

EMPHASIS = {
    "technical_skills_weight": 30,
    "soft_skills_weight": 5,
    "experience_weight": 20,
    "education_weight": 15,
    "language_proficiency_weight": 15,
    "certifications_weight": 5,
    "location_weight": 10
}