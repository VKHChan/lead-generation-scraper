FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

# Install Microsoft ODBC Driver for SQL Server
RUN apt-get update && apt-get install -y unixodbc curl gnupg \
  && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl -sSL https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y msodbcsql18