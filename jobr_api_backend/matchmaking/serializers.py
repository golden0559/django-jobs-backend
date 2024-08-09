from rest_framework import serializers
from .models import Match, ApplyVacancy
from accounts.models import Employee, Employer
from vacancies.models import Vacancy


class MatchSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.user.username", read_only=True)
    employer_name = serializers.CharField(source="employer.company_name", read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'employee', 'employer', 'match_score', 'match_type', 'created_at', 'employee_name', 'employer_name']


class ApplyVacancySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.user.username", read_only=True)
    vacancy_title = serializers.CharField(source="vacancy.title", read_only=True)

    class Meta:
        model = ApplyVacancy
        fields = ['id', 'employee', 'vacancy', 'applied_at', 'employee_name', 'vacancy_title']
