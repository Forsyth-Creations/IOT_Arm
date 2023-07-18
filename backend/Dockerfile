FROM python:3.10-slim
# Set the working directory
WORKDIR /app

RUN pip install poetry==1.4.2

# Copy the requirements file
COPY  main.py pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false --local && poetry install

# # Expose the port
EXPOSE 8000


