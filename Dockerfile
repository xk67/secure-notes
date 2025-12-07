FROM python:3.13-slim

WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY requirements.txt entrypoint.sh .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN useradd -M -r appuser && chown -R appuser:appuser .
USER appuser
 
EXPOSE 8000
 
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]