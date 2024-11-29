from fastapi import FastAPI
from pydantic import BaseModel

import uvicorn
import resume_matcher
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

class ResumeJobMatch(BaseModel):
    resume_url: str
    jd: str
class Assessment(BaseModel):
    question: str
    answer: str

class Resume(BaseModel):
    url: str

class JD(BaseModel):
    jd: str

@app.post("/evaluate_candidate_answer")
async def evaluate_candidate_answer(assessment: Assessment):
    answer_score = resume_matcher.evaluate_candidate_answer(question=assessment.question, answer=assessment.answer)
    return answer_score

@app.post("/match_resume_to_job")
async def match_resume_to_job(resumeJobMatch: ResumeJobMatch):
    match = resume_matcher.process_single_resume(job_desc=resumeJobMatch.jd, resume_url=resumeJobMatch.resume_url)
    return match

@app.post("/extract_candidate_profile")
async def extract_candidate_profile(resume: Resume):
    text, images = resume_matcher.extract_text_and_image_from_pdf(resume.url)
    candidate_profile = resume_matcher.extract_candidate_profile(text)
    return candidate_profile

@app.post("/extract_job_requirements")
async def extract_job_requirements(jd: JD):
    job_requirements = resume_matcher.extract_job_requirements(jd.jd)
    return job_requirements

@app.post("/generate_role_questions")
async def generate_role_questions(jd: JD):
    job_requirements = resume_matcher.generate_role_questions(jd.jd)
    return job_requirements

@app.post("/generate_candidate_questions")
async def generate_candidate_questions(resumeJobMatch: ResumeJobMatch):
    job_requirements = resume_matcher.generate_candidate_questions(job_desc=resumeJobMatch.jd, resume_url=resumeJobMatch.resume_url)
    return job_requirements

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5050)
