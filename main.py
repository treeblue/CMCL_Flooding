import requests as R

root = "https://environment.data.gov.uk/flood-monitoring"

req = R.get("https://environment.data.gov.uk/flood-monitoring/id/stations")
print(req.text)