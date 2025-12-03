FROM python:3.13-slim

WORKDIR /usr/src/app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY requirements.txt manage.py .
COPY sse ./sse
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -M -r appuser && chown -R appuser:appuser .
USER appuser
 
EXPOSE 8000
 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]