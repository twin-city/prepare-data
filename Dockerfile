FROM python:3.7-slim

# Install Fastapi
RUN pip install fastapi uvicorn

# Install prepare_data package
COPY . .
RUN pip install -r requirements.txt
RUN pip install -e .
EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
