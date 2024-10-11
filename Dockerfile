FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/

ENV SUPERUSER_USERNAME=ahmed
ENV SUPERUSER_EMAIL=ahmed.abdulq02@gmail.com
ENV SUPERUSER_PASSWORD=ahm123!*

EXPOSE 8000

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Run the Django development server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "wellence_project.asgi:application"]