# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Default command to run your app
CMD ["python", "app.py"]