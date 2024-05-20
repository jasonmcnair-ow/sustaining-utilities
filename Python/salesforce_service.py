from simple_salesforce import Salesforce
from datetime import datetime

username = 'xxxx'
password = 'xxxx'
security_token = 'xxxx'

sf = Salesforce(username=username, password=password,
                security_token=security_token)

case_select_minimal = "SELECT Id, CaseNumber FROM Case"
# case_select = "SELECT Id, CaseNumber, Status, ContactEmail, Description, CreatedDate, Latest_Update_Date__c, Billing_Code__c, (SELECT Id, Subject, HtmlBody, TextBody, MessageDate FROM EmailMessages) FROM Case"
case_select_full = "SELECT Id, CaseNumber, Status, ContactEmail, Subject, Description, CreatedDate, Latest_Update_Date__c, Billing_Code__c, (SELECT Id, Subject, TextBody, MessageDate FROM EmailMessages) FROM Case"

def single_quote_and_comma_separate(array):
    return ','.join("'" + value + "'" for value in array)

def ticket_lookup(ticket_numbers):
    ticket_dict = {}
    # loop through ticket numbers
    for ticket_number in ticket_numbers:
        # get the ticket reference
        ticket_ref = sf.query(
            f"{case_select_minimal} WHERE CaseNumber = '{ticket_number}'")
        # add the ticket reference to TICKET_LOOKUP
        ticket_dict[ticket_number] = ticket_ref['records'][0]['Id']
    return ticket_dict

def create_time_entries(records):
    for record in records:
        print(record)
        # stripping out and replacing excel formatted date
        date = datetime.strptime(record['date'], '%m/%d/%Y')
        sf.Time_Entry__c.create({ 'Date__c': date.strftime('%Y-%m-%d'), 'Hours_Worked__c': record['Hours Worked'], 'Description__c': record['Description'], 'Subject__c': record['Subject'], 'Ticket__c': record['ticket'], 'Effort_Type__c': record['effortType'] })
        
def get_daterange_clause(field, start: datetime, end: datetime):
    start_datetime = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_datetime = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    return f"{field} >= {start_datetime} AND {field} <= {end_datetime}"

def ticket_export_by_numbers(ticket_nums):
    ticket_nums_string = single_quote_and_comma_separate(ticket_nums)

    ticket_refs = sf.query_all(f"{case_select_full} WHERE CaseNumber in ({ticket_nums_string})")
    
    return ticket_refs

def ticket_export(billing_codes, start: datetime, end:datetime=datetime.now()):
    billing_codes_string = single_quote_and_comma_separate(billing_codes)
    createddate_clause = get_daterange_clause("CreatedDate", start, end)
    # modifieddate_clause = get_daterange_clause("LastModifiedDate", start, end)
    modifieddate_clause = get_daterange_clause("Latest_Update_Date__c", start, end)

    ticket_refs = sf.query_all(f"{case_select_full} WHERE Billing_Code__c IN ({billing_codes_string}) AND (({createddate_clause}) OR ({modifieddate_clause}))")

    ticket_ids = [d['Id'] for d in ticket_refs["records"]]
    ticket_ids_string = single_quote_and_comma_separate(ticket_ids)

    # print(ticket_ids)

    casefeed_query = f"SELECT Id, Type, Body, ParentId FROM CaseFeed where ParentId IN ({ticket_ids_string}) AND (Type <> 'EmailMessageEvent')"

    casefeeds = sf.query_all(casefeed_query)

    ticket_records = []

    for ticket_ref_record in ticket_refs["records"]:
        ticket_id = ticket_ref_record["Id"]

        ticket_casefeed = [i for i in casefeeds["records"] if i.get('ParentId') == ticket_id]

        ticket_ref_record["CaseFeed"] = ticket_casefeed

        ticket_records.append(ticket_ref_record)


    return ticket_records
