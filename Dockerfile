# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYDEVD_USE_CYTHON=NO \
    PYDEVD_USE_FRAME_EVAL=NO

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port [REDACTED_PORT] available to the world outside this container
EXPOSE [REDACTED_PORT]

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["python", "api.py"]
