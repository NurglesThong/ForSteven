# app/Dockerfile
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the Dash app
CMD ["python", "app.py"]
