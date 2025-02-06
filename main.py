from fastapi import FastAPI
from pydantic import BaseModel
from langsmith import traceable
import uvicorn
import resume_matcher
import logging
import uuid, sys
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

@traceable
@app.post("/evaluate_candidate_answer")
async def evaluate_candidate_answer(assessment: Assessment):
    request_id = uuid.uuid4().hex
    answer_score = resume_matcher.evaluate_candidate_answer(question=assessment.question, answer=assessment.answer, request_id=request_id)
    return answer_score

@traceable
@app.post("/match_resume_to_job")
async def match_resume_to_job(resumeJobMatch: ResumeJobMatch):
    request_id = uuid.uuid4().hex
    match = resume_matcher.process_single_resume(job_desc=resumeJobMatch.jd, resume_url=resumeJobMatch.resume_url, request_id=request_id)
    return match

@traceable
@app.post("/extract_candidate_profile")
async def extract_candidate_profile(resume: Resume):
    request_id = uuid.uuid4().hex
    candidate_profile = resume_matcher.extract_candidate_profile(resume.url, request_id=request_id)
    return candidate_profile

@traceable
@app.post("/extract_job_requirements")
async def extract_job_requirements(jd: JD):
    request_id = uuid.uuid4().hex
    job_requirements = resume_matcher.extract_job_requirements(jd.jd, request_id=request_id)
    return job_requirements

@traceable
@app.post("/generate_role_questions")
async def generate_role_questions(jd: JD):
    request_id = uuid.uuid4().hex
    job_requirements = resume_matcher.generate_role_questions(jd.jd, request_id=request_id)
    return job_requirements

@traceable
@app.post("/generate_candidate_questions")
async def generate_candidate_questions(resumeJobMatch: ResumeJobMatch):
    request_id = uuid.uuid4().hex
    job_requirements = resume_matcher.generate_candidate_questions(job_desc=resumeJobMatch.jd, resume_url=resumeJobMatch.resume_url, request_id=request_id)
    return job_requirements

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "ok"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5050)
