FROM python:3.12-bullseye

WORKDIR /app
COPY . .

RUN pip install pipenv 
RUN pipenv sync

RUN pipenv run python manage.py collectstatic --noinput

EXPOSE 8000

# Command to run the Python script
CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:8000", "jobr_api_backend.wsgi:application"]