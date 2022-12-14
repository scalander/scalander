# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8.15-buster

EXPOSE 8082

# read the environment
ARG MODE
ENV MODE $MODE

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN apt update && apt install -y build-essential
COPY requirements.txt .
# install mysql
RUN apt update
RUN apt install -y default-mysql-client
# install requirements
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# create static paths
RUN mkdir static

# collect static files; they ask for confirmation so we confirm by saying yes
# yes yes says yes instead of y for yes. Yes that's how that works.
RUN yes yes | python manage.py collectstatic

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# scheduling takes a *long time* TODO
CMD ["gunicorn", "-b :8082", "-w 4", "-t 8000", "backend.wsgi"]
