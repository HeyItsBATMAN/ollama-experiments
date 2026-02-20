# Task

Extract metadata in json format

CLASSIFICATION OPTIONS - purpose of document
- Political Correspondence - letters between political parties
- Official Records - reports without addressee
- Printed Material - media articles - books
- Legal Documents - law - decreet

OUTPUT FORMAT:
{
  "classification": "",
  "language": "",
  "summary": "",
  "issue_date": "",
  "places": "",
  "signature:
}

INSTRUCTIONS:
- Choose classification from options above
- Language: German or Italian
- Date: YYYY-MM-DD format (or empty string if missing)
- Place: city name (or empty string if missing)
- Signature: name or empty if missing
