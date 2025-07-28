# Use an official, lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project context (including main.py and the utils folder)
COPY . .

# Specify the command to run when the container starts
CMD ["python", "main.py"]```

With these files properly arranged in your project folder, your main.py script will be able to find and use the extract_structure function, and your Docker container will build and run correctly.