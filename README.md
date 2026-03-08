# API QA Probe

`API QA Probe` is a portfolio-ready Python project for API testing and QA automation.

It loads API test definitions from JSON, validates mock responses against expected status codes and field assertions, and generates a readable regression-style report.

## Best fit roles

- QA Analyst / Junior QA Engineer
- API Test Engineer
- QA Automation Engineer
- Technical Support roles that need API debugging skills

## Why it matters

Many teams have API endpoints and example payloads, but no lightweight way to:

- verify expected status codes
- check required fields
- detect contract mismatches
- produce a repeatable regression summary

This project turns a simple test definition file into structured QA output.

## Features

- Load API test cases from JSON
- Validate status codes
- Validate required fields
- Validate field equality assertions
- Summarize pass / fail results
- Generate Markdown or JSON reports

## Quick start

```powershell
cd "C:\Users\Administrator\Documents\New project\api_qa_probe"
python -m src.api_qa_probe.cli run sample_data\api_cases.json --format markdown
python -m unittest discover -s tests
```

## Example output

```powershell
python -m src.api_qa_probe.cli run sample_data\api_cases.json --format markdown --output outputs\api_report.md
```

## What this project demonstrates

- API-focused QA thinking
- structured validation rules
- regression-style reporting
- Python test automation fundamentals
