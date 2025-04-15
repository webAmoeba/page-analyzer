### Hexlet tests and linter status:
[![Actions Status](https://github.com/webAmoeba/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/webAmoeba/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=webAmoeba_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=webAmoeba_python-project-83)

### Deployed:
[onrender.com](https://python-project-83-qku7.onrender.com/)

# Page Analyzer:
Welcome to the Page Analyzer project! This repository contains a web application designed to analyze web pages and provide detailed insights into their structure and content.

## Requirements:
To run this project, you need to have the following software installed:
- Python >=3.10
- Uv

## Preparation:
Create .env file with code kind of:
```bash
export DATABASE_URL=postgresql://admin:password@localhost:5432/db_project_83
export SECRET_KEY=secretKey
```
Create PostgreSQL database using settings from your .env file

## Installation:
To set up the project, navigate to the project directory and run the following command:
```bash
make install
```

## Local run:
```bash
make sql
```
```bash
make dev
```