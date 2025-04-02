# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application
COPY . /app/

# Expose backend port
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]