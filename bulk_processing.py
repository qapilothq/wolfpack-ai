from resume_matcher import extract_text_and_image_from_pdf, unify_format, match_resume_to_job, check_website, get_score_details, unify_single_resume, match_single_resume
import json5, requests, os, logging, json
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

def worker(args):
    file, job_desc, font_styles, generate_pdf = args
    try:
        extracted_data = extract_text_and_image_from_pdf(file)
        unified_resume, resume_images = unify_format(extracted_data, font_styles, generate_pdf)
        
        if not unified_resume:
            return (os.path.basename(file), 0, "🔴", "red", "Error: Failed to unify resume format", "", "", [])
        
        result = match_resume_to_job(unified_resume, job_desc, file, resume_images)
         
        # Use json5 to parse the result
        if isinstance(result, str):
            result = json5.loads(result)
        
        score = result.get('score', 0)
        match_reasons = result.get('match_reasons', '')
        website = result.get('website', '')
        red_flags = result.get('red_flags', [])
        
        # Check if the website is accessible
        if website:
            is_accessible, updated_url = check_website(website)
            if not is_accessible:
                score = max(0, score - 25)  # Reduce score, but not below 0
                website = f"{updated_url} (inactive)"
            else:
                website = updated_url
                # Fetch website content
                try:
                    response = requests.get(website, timeout=5)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    website_text = soup.get_text(separator=' ', strip=True)
                    
                    # Combine unified_resume and website_text
                    combined_text = f"{unified_resume}\n\nWebsite Content:\n{website_text}"
                    
                    # Re-run match_resume_to_job with combined_text
                    result = match_resume_to_job(combined_text, job_desc, file, resume_images)
                    if isinstance(result, str):
                        result = json5.loads(result)
                    score = result.get('score', 0)
                    match_reasons = result.get('match_reasons', '')
                except Exception as e:
                    logging.error(f"Error fetching website content for {file}: {str(e)}")
        
        emoji, color, label = get_score_details(score)
        return (os.path.basename(file), score, emoji, color, label, match_reasons, website, red_flags)
    except json.JSONDecodeError as je:
        error_msg = f"JSON Decode Error: {str(je)}"
        logging.error(f"Error processing {file}: {error_msg}")
        return (os.path.basename(file), 0, "🔴", "red", error_msg, "", "", [])
    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        logging.error(f"Error processing {file}: {error_msg}")
        return (os.path.basename(file), 0, "🔴", "red", error_msg, "", "", [])

import concurrent.futures

import concurrent.futures
from functools import partial

def process_resumes(job_desc, pdf_files, font_styles, generate_pdf):
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(os.cpu_count(), len(pdf_files))) as executor:
        # First, parallelize the unification process
        unified_futures = {executor.submit(unify_single_resume, file, font_styles, generate_pdf): file for file in pdf_files}
        
        unified_results = {}
        with tqdm(total=len(pdf_files), desc="Unifying resumes", unit="file") as pbar:
            for future in concurrent.futures.as_completed(unified_futures):
                file = unified_futures[future]
                try:
                    unified_resume, resume_images = future.result()
                    unified_results[file] = (unified_resume, resume_images)
                except Exception as e:
                    unified_results[file] = (None, None)
                pbar.update(1)
        
        # Then, parallelize the matching process
        match_func = partial(match_single_resume, job_desc)
        match_futures = {executor.submit(match_func, file, *unified_results[file]): file for file in pdf_files}
        
        results = []
        with tqdm(total=len(pdf_files), desc="Matching resumes", unit="file") as pbar:
            for future in concurrent.futures.as_completed(match_futures):
                file = match_futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    basename = os.path.basename(file)[:20]
                    results.append((basename, 0, "🔴", "red", f"Error: {str(e)}", "", "", []))
                pbar.update(1)
    
    return results