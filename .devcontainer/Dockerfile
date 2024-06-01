FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.10

EXPOSE 8000

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install docker \
  /workspace/cabinet  && apt-get -y install --no-install-recommends postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

CMD sudo chmod 666 /var/run/docker.sock