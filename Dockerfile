FROM python:3.11.5

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/health/ || exit 1   

# CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0"]
CMD ["gunicorn", "-w", "4", "main:app", "-b", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker"]
