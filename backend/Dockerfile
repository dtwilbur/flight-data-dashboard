FROM python:3.11-slim

# Create working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app /app/app

# Expose port
EXPOSE 8000

# Default command runs the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]