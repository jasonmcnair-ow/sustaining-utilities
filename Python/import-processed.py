import csv

from salesforce_service import create_time_entries

records = []

with open('time-entries-preprocess-output.csv', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
#         print(row)
        records.append(row)

create_time_entries(records)