from simple_salesforce import Salesforce
from datetime import datetime

username = 'xxxx'
password = 'xxxx'
security_token = 'xxxx'

sf = Salesforce(username=username, password=password,
                security_token=security_token)

def ticket_lookup(ticket_numbers):
    ticket_dict = {}
    # loop through ticket numbers
    for ticket_number in ticket_numbers:
        # get the ticket reference
        ticket_ref = sf.query(
            f"SELECT Id, CaseNumber FROM Case WHERE CaseNumber = '{ticket_number}'")
        # add the ticket reference to TICKET_LOOKUP
        ticket_dict[ticket_number] = ticket_ref['records'][0]['Id']
    return ticket_dict

def create_time_entries(records):
    for record in records:
        print(record)
        # stripping out and replacing excel formatted date
        date = datetime.strptime(record['date'], '%m/%d/%Y')
        sf.Time_Entry__c.create({ 'Date__c': date.strftime('%Y-%m-%d'), 'Hours_Worked__c': record['Hours Worked'], 'Description__c': record['Description'], 'Subject__c': record['Subject'], 'Ticket__c': record['ticket'] })
