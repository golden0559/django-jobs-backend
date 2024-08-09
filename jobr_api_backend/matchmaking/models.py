from django.db import models
from accounts.models import Employee, Employer
from vacancies.models import Vacancy


class Match(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    match_score = models.PositiveIntegerField()  # Score between 0 and 100
    match_type = models.CharField(max_length=50, choices=[
        ('employee_to_employer', 'Employee to Employer'),
        ('employer_to_employee', 'Employer to Employee')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user.username} - {self.employer.company_name} - Match score: {self.match_score}"


class ApplyVacancy(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='applied_vacancies_matchmaking'  # Unique related_name
    )
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='applications_matchmaking'  # Unique related_name
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user.username} applied for {self.vacancy.title} on {self.applied_at}"
