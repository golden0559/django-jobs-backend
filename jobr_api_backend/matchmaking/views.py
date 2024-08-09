from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Match, ApplyVacancy
from accounts.models import Employee, Employer
from vacancies.models import Vacancy
from .serializers import MatchSerializer, ApplyVacancySerializer
from .utils import calculate_match, enhanced_match_score, get_best_matching_vacancies, apply_for_vacancy


class MatchViewSet(ViewSet):
    """
    ViewSet for Match-related operations.
    """

    @action(detail=True, methods=['get'])
    def hello(self, request, pk=None):
        """
        GET /matches/{pk}/employee_matches/
        Fetch best matches for a specific employee.
        """
        
        return Response("hello")

    @action(detail=True, methods=['get'])
    def employee_matches(self, request, pk=None):
        """
        GET /matches/{pk}/employee_matches/
        Fetch best matches for a specific employee.
        """
        employee = get_object_or_404(Employee, pk=pk)
        matches = Match.objects.filter(employee=employee).order_by('-match_score')
        serialized_data = [
            {"employer": match.employer.company_name, "match_score": match.match_score}
            for match in matches
        ]
        return Response(serialized_data)

    @action(detail=True, methods=['get'])
    def employer_matches(self, request, pk=None):
        """
        GET /matches/{pk}/employer_matches/
        Fetch best matches for a specific employer.
        """
        employer = get_object_or_404(Employer, pk=pk)
        matches = Match.objects.filter(employer=employer).order_by('-match_score')
        serialized_data = [
            {"employee": match.employee.user.username, "match_score": match.match_score}
            for match in matches
        ]
        return Response(serialized_data)

    @action(detail=True, methods=['get'])
    def best_matches(self, request, pk=None):
        """
        GET /matches/{pk}/best_matches/
        Get enhanced best matches for an employee.
        """
        employee = get_object_or_404(Employee, pk=pk)
        best_matches = []

        for vacancy, vacancy_score in get_best_matching_vacancies(employee):
            employer = vacancy.employer
            match_score = enhanced_match_score(employee, employer)

            best_matches.append({
                "employer": employer.company_name,
                "match_score": match_score,
                "vacancy_score": vacancy_score,
                "vacancy_title": vacancy.title,
                "vacancy_location": vacancy.location,
                "vacancy_salary": vacancy.salary
            })

        return Response({"best_matches": best_matches})

class ApplyVacancyViewSet(ViewSet):
    """
    ViewSet for handling job applications.
    """

    @action(detail=False, methods=['post'])
    def apply(self, request):
        """
        POST /applications/apply/
        Allows an employee to apply for a specific vacancy.
        """
        employee_id = request.data.get("employee_id")
        vacancy_id = request.data.get("vacancy_id")

        employee = get_object_or_404(Employee, pk=employee_id)
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

        result = apply_for_vacancy(employee, vacancy)
        return Response({"result": result})