import json

def get_linkedin_location(linkedin_geo):
    try:
        location = ""
        if linkedin_geo:
            location = linkedin_geo.get("full", "")
        return location.strip()
    except Exception as e:
        return ""
    
# getting the latest education only as single string
def get_linkedin_education(linkedin_education):
    try:
        education = ""
        if len(linkedin_education) > 0:
            latest_education = linkedin_education[0]
            education = f"{latest_education.get("degree")} in {latest_education.get("fieldOfStudy")} from {latest_education.get("schoolName")}"
        return education.strip()
    except Exception as e:
        return ""
    
def get_linkedin_positions(linkedin_positions):
    try:
        positions = ""
        if len(linkedin_positions) > 0:
            for position in linkedin_positions:
                position_text = f"{position.get("title")} at {position.get("companyName")}, {position.get("location")} from {position.get("start").get("year")}"
                position_end_year = position.get("end").get("year")
                if position_end_year > 0:
                    position_text = position_text + f" to {position_end_year} | "
                else :
                    position_text = position_text + f" to now | "
                positions = positions + position_text
            
        return positions.strip()

    except Exception as e:
        return ""

def get_linkedin_skills(linkedin_skills):
    try:
        skills = ""
        if len(linkedin_skills) > 0:
            for skill in linkedin_skills:
                skills = skills + skill.get("name", "") + " | "

        return skills.strip()
    except Exception as e:
        return ""
    
def get_linkedin_courses(linkedin_courses):
    try:
        courses = ""
        if len(linkedin_courses) > 0:
            for course in linkedin_courses:
                courses = courses + course.get("name", "") + " | "

        return courses.strip()
    except Exception as e:
        return ""
    
def get_linkedin_certifications(linkedin_certifications):
    try:
        certifications = ""
        if len(linkedin_certifications) > 0:
            for certification in linkedin_certifications:
                certifications = certifications + f"{certification.get("name", "")} from {certification.get("authority", "")}" + " | "

        return certifications.strip()
    except Exception as e:
        return ""
    
def get_linkedin_honors(linkedin_honors):
    try:
        honors = ""
        if len(linkedin_honors) > 0:
            for honor in linkedin_honors:
                honors = honors + honor.get("title", "") + f" in {honor.get("issuedOn").get("year")} | "

        return honors.strip()
    except Exception as e:
        return ""