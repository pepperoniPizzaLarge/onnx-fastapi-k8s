FROM python:3.11.11

# Set working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run default command - start FastAPI with Uvicorn 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]