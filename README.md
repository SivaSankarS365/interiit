# Run The Server
python
python app.py


# Backend API

| Route       | Method     | Returns |
| ----------- | ----------- | --------|
| /      | get       | test route |
| /search   | get   | searches details of thios company and returns it's cik, company_name, company_logo, ticker |

# Metric Extraction From Reports

Libraries used for Extracting Metrics
1) Beautiful Soup
2) RegEx

Classes
1) app.py: Wraps code to perform metric extraction from html, file.
2) Link_Manager.py : Gets file from link and start metric extraction.
3) wrapper.py : Script to handle extraction.
