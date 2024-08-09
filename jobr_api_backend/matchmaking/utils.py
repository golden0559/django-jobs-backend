from .models import Match
from accounts.models import Employee, Employer, Review
from .models import ApplyVacancy
from vacancies.models import Vacancy, ContractType, Function, Language, Skill
def calculate_match(employee: Employee, employer: Employer) -> int:
    # Initialize match score
    score = 0

    # Matching Contract Type (10 points)
    if employee.contract_type == employer.contract_type:
        score += 10

    # Matching Function (15 points)
    if employee.function == employer.function:
        score += 15

    # Matching Skills (20 points)
    employee_skills = set(employee.skill.all())
    employer_skills = set(employer.skill.all())
    common_skills = employee_skills.intersection(employer_skills)
    score += len(common_skills) * 5  # Each shared skill adds 5 points

    # Matching Language Proficiency (15 points)
    employee_languages = set(employee.language.all())
    employer_languages = set(employer.language.all())
    common_languages = employee_languages.intersection(employer_languages)
    score += len(common_languages) * 5  # Each shared language adds 5 points

    # Location Proximity (20 points)
    if employee.latitude and employee.longitude and employer.coordinates:
        employee_location = (employee.latitude, employee.longitude)
        employer_location = (employer.coordinates['latitude'], employer.coordinates['longitude'])
        
        # Calculate distance between locations (in km)
        from geopy.distance import geodesic
        distance = geodesic(employee_location, employer_location).km
        
        if distance <= 50:  # If within 50km, give a match score
            score += 10
        elif distance <= 200:  # If within 200km, give a smaller score
            score += 5

    # Experience Level (Optional: add more fields to Employee/Employer for experience level)
    # Assuming employees have an `experience` field
    if hasattr(employee, 'experience') and hasattr(employer, 'required_experience'):
        if employee.experience >= employer.required_experience:
            score += 10

    # Normalize the score to be between 0 and 100
    max_score = 100
    match_score = min(score, max_score)  # Ensure it doesn't exceed 100

    return match_score


def create_match(employee: Employee, employer: Employer):
    match_score = calculate_match(employee, employer)
    match = Match.objects.create(employee=employee, employer=employer, match_score=match_score, match_type='employee_to_employer')
    return match

def get_employee_reviews(employee):
    """Fetch reviews for an employee and calculate average rating."""
    reviews = Review.objects.filter(employee=employee)
    total_rating = sum([review.rating for review in reviews])
    return total_rating / reviews.count() if reviews.exists() else 0


def get_employer_reviews(employer):
    """Fetch reviews for an employer and calculate average rating."""
    reviews = Review.objects.filter(employer=employer)
    total_rating = sum([review.rating for review in reviews])
    return total_rating / reviews.count() if reviews.exists() else 0


def calculate_reputation_score(entity_type, entity):
    """Calculate reputation score for employee or employer based on reviews."""
    rating = get_employee_reviews(entity) if entity_type == 'employee' else get_employer_reviews(entity)
    return int((rating / 5) * 100)  # Rating is between 1 and 5, converting to a score out of 100


# Vacancy-related utility functions
def get_best_matching_vacancies(employee):
    """Get the best matching vacancies for an employee."""
    vacancies = Vacancy.objects.all()
    best_matches = []

    for vacancy in vacancies:
        vacancy_score = 0

        # Matching contract type
        if employee.contract_type == vacancy.contract_type:
            vacancy_score += 10

        # Matching function
        if employee.function == vacancy.function:
            vacancy_score += 15

        # Matching skills
        employee_skills = set(employee.skill.all())
        vacancy_skills = set(vacancy.skill.all())
        common_skills = employee_skills.intersection(vacancy_skills)
        vacancy_score += len(common_skills) * 5

        # Matching languages
        employee_languages = set(employee.language.all())
        vacancy_languages = set(vacancy.language.all())
        common_languages = employee_languages.intersection(vacancy_languages)
        vacancy_score += len(common_languages) * 5

        # Location proximity
        if employee.latitude and employee.longitude and vacancy.latitude and vacancy.longitude:
            employee_location = (employee.latitude, employee.longitude)
            vacancy_location = (vacancy.latitude, vacancy.longitude)
            distance = geodesic(employee_location, vacancy_location).km
            if distance <= 50:
                vacancy_score += 10
            elif distance <= 200:
                vacancy_score += 5

        best_matches.append((vacancy, vacancy_score))

    # Sort by score, highest first
    best_matches.sort(key=lambda x: x[1], reverse=True)
    return best_matches


def apply_for_vacancy(employee, vacancy):
    """Allow an employee to apply for a vacancy."""
    if ApplyVacancy.objects.filter(employee=employee, vacancy=vacancy).exists():
        return "Already applied"
    ApplyVacancy.objects.create(employee=employee, vacancy=vacancy)
    return "Application successful"


def create_vacancy(employer, title, contract_type, function, skills, salary, description, language, location, latitude, longitude):
    """Create a new vacancy listing."""
    vacancy = Vacancy.objects.create(
        title=title,
        contract_type=contract_type,
        function=function,
        salary=salary,
        description=description,
        employer=employer,
        language=language,
        skill=skills,
        location=location,
        latitude=latitude,
        longitude=longitude
    )
    return vacancy


# Matchmaking-related utility functions
def enhanced_match_score(employee, employer):
    """Calculate an enhanced match score between an employee and an employer."""
    base_match_score = calculate_match(employee, employer)
    employee_reputation = calculate_reputation_score('employee', employee)
    employer_reputation = calculate_reputation_score('employer', employer)

    # Adjust the base score based on reputation
    score = base_match_score + ((employee_reputation + employer_reputation) // 2)

    # Add points based on best matching vacancy
    best_vacancy_score = get_best_matching_vacancies(employee)[0][1]  # Get the best match score
    score += best_vacancy_score // 2  # 50% weight for best vacancy match

    return min(score, 100)