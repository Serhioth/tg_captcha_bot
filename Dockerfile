FROM python:3.11-slim
# Specify the working directory 
WORKDIR /app
# Copying requirements.txt to container
COPY requirements.txt ./
# Install dependencies
RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir
# Copy project to container
COPY . .
# Set PYTHONPATH environment variable to the working directory
ENV PYTHONPATH=/app
# Make port 8181 available to the world outside this container
EXPOSE 8181
# Run main.py when the container launches
CMD ["python", "./bot/main.py"]
