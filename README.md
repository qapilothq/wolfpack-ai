# Wolf-Pack AI

## Overview
This is a FastAPI-based application designed to analyze Resumes and Job Descriptions. This application provides the following features:
1. Evaluates Candidate answers in the evaluation
2. Matches a resume to a Job Description
3. Extracts Candidate profile in a structured format from Resume
4. Extracts Job requirements in a structured format from Job Description
5. Generates Role/Job specific questions for candidate assessment
6. Generates resume specific questions for candidate assessment


## API Endpoints

### 1. Evaluate Candidate Answer

- **Endpoint:** `/evaluate_candidate_answer`
- **Method:** `POST`
- **Description:** Evaluates a candidate's answer to a given question based on predefined metrics.
- **Request Body:**
  - `question` (string): The question posed to the candidate.
  - `answer` (string): The candidate's response to the question.
- **Response:** JSON object containing scores for various evaluation metrics.

### 2. Match Resume to Job

- **Endpoint:** `/match_resume_to_job`
- **Method:** `POST`
- **Description:** Matches a candidate's resume to a job description and provides a score and match reasons.
- **Request Body:**
  - `resume_url` (string): URL of the candidate's resume.
  - `jd` (string): Job description text.
- **Response:** JSON object containing the match score, reasons, and any red flags.

### 3. Extract Candidate Profile

- **Endpoint:** `/extract_candidate_profile`
- **Method:** `POST`
- **Description:** Extracts structured candidate profile information from a resume.
- **Request Body:**
  - `url` (string): URL of the candidate's resume.
- **Response:** JSON object containing the extracted candidate profile.

### 4. Extract Job Requirements

- **Endpoint:** `/extract_job_requirements`
- **Method:** `POST`
- **Description:** Extracts key job requirements from a job description.
- **Request Body:**
  - `jd` (string): Job description text.
- **Response:** JSON object containing structured job requirements.

### 5. Generate Role Questions

- **Endpoint:** `/generate_role_questions`
- **Method:** `POST`
- **Description:** Generates role-based questions for candidate assessment based on the job description.
- **Request Body:**
  - `jd` (string): Job description text.
- **Response:** JSON object containing a list of questions.

### 6. Generate Candidate Questions

- **Endpoint:** `/generate_candidate_questions`
- **Method:** `POST`
- **Description:** Generates candidate-specific questions for assessment based on the resume and job description.
- **Request Body:**
  - `resume_url` (string): URL of the candidate's resume.
  - `jd` (string): Job description text.
- **Response:** JSON object containing a list of questions.

## Credit
This is built using [Resume Job Matcher](https://github.com/sliday/resume-job-matcher)

## Contributing
We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact
For questions or support, please contact **[contactus@qapilot.com](mailto:contactus@qapilot.com)**.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.