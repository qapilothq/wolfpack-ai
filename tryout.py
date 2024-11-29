import resume_matcher
import PyPDF2

# Example usage
pdf_file_path = '/Users/surendranath.j/work/repos/resume-job-matcher/Profiles/React js/Adarsh_Kp _cv.pdf'
print("reading resume")
resume_text, resume_images = resume_matcher.extract_text_and_image_from_pdf(pdf_file_path)
unified_resume, _ = resume_matcher.unify_format((resume_text, resume_images), {}, generate_pdf=False)
print("Unified Resume -- \n")
print(unified_resume)

print("reading JD")
# Open the file in read mode
with open('job_description.txt', 'r') as file:
    # Read the contents of the file into a string
    jd = file.read()
job_requirements = resume_matcher.extract_job_requirements(job_desc=jd)
print(job_requirements)
print("ranking JD")
print(resume_matcher.rank_job_description(job_requirements))
print("matching resume to job")
print("\n\n")
print(resume_matcher.match_resume_to_job(unified_resume, jd, pdf_file_path, None, None))