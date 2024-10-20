# Use a lightweight base image with Python 3.9
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the inference script into the working directory
COPY inference.py .

# Expose a port if needed for APIs (e.g., Flask)
# EXPOSE 8080

# Run the inference script when the container starts
CMD ["python", "inference.py"]

