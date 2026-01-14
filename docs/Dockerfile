FROM python:3.13-slim

WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./docs ./docs
COPY mkdocs.yml .

RUN pip install --no-cache-dir mkdocs

RUN useradd -M -r appuser && chown -R appuser:appuser .
USER appuser

EXPOSE 3000

CMD ["mkdocs", "serve", "-a", "0.0.0.0:3000"]
