FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

# Run the Django development server
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 wellence_project.asgi:application"]