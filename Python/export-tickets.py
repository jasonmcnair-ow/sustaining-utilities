import json
from datetime import datetime
import os
from salesforce_service import ticket_export

# tickets_nums = ['LT0568440', 'LT0577651', 'LT0555064', 'LT0569845']
tickets_nums = ['LT0569845']
# tickets_nums = ['LT0555064']

file_path = "C:\\Users\\jason.mcnair\\OneDrive - MMC\\Documents - RCGA-Product Engineering\\General\\Salesforce\\"
# file_path = "C:\\code\\sustaining-utilities\\Python\\ticketoutputs\\"

code_folders = {
    "AHLD-0006": "AHLD-0006--ProductionPlanning",
    "AHLD-0007": "AHLD-0007--AllocationRepository"
}

# cycle through keys in code_folders
for key in code_folders:
    print(key, code_folders[key])

    # create a directory for code_folders[key] if it doesn't exist
    os.makedirs(f"{file_path}{code_folders[key]}", exist_ok=True)

    results = ticket_export([key], datetime.fromisoformat('2024-04-04'))

    for ticket in results:
        with open(f"{file_path}{code_folders[key]}\{ticket['CaseNumber']}.txt", "w") as file:
            json.dump(ticket, file, indent=4)




# billing_codes = ["BJH00411","AHQ02911"]
# billing_codes = ["AHQ02911"]
# billing_codes = ["AHLD-0006"]

# # result = ticket_export_by_numbers(tickets_nums)
# result = ticket_export(billing_codes, datetime.fromisoformat('2024-04-04'))

# with open(file_path, "w") as file:
#     json.dump(result, file, indent=4)

# with open("casefeeds.json", "w") as file:
#     json.dump(casefeeds, file, indent=4)

# json_result = json.dumps(result, indent=4)

# print(json_result)