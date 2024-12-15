from cmath import log
from fileinput import filename
import csv
import time
import pandas as pd

from salesforce_service import ticket_lookup

TICKET_RATIOS = {
    "LT0137169": 0.5,
    "LT0088440": 0.25,
    "LT0492226": 0.25
}

RCGNA_TICKETS = [
    '5004100000eKpyb',
    '5004100000Jony7',
    '5004U00001AoOeQ'
]

TICKET_LOOKUP = {
    "OW:General": "5004100000D8Ml1",
    "OW:Recharge": "5002M00001CEm55",
    "OW:DigMeetings": "5004100000Y6kg8",
    "OW:Holiday": "5002M00001MozIZ",
    "OW:PTO": "5002M00000y3usS",
    "OW:Sick": "5002M00001KjTMX",
    "OW:Training": "5002M00001NzmMb",
    "OW:PassReset": "5002M00001XFO9v",
    "OW:DSS": "5002M00001Ze20U",
    "AHQ:Alloc": "5004100000D8RtMAAV",
    "AHQ:PP": "5004100000eKpyb",
    "AHQ:AOv3": "5004100000Jony7",
    # "BJH:InputCost": "5002M00001bAd0x",
    "BJH:ICM": "5004U00001AoOeQ",
    "AER51101": "5002M00001bu9JV",
    # "LT0557570": "5004U00001AnTd1",
}

def get_ticket_number_from_subproject(subproject):
    subproject_split = subproject.split(':')
    # print(subproject_split)
    if len(subproject_split) > 1 and subproject_split[1].startswith('LT'):
        return subproject_split[1]


def get_ticket_for_row(row):
    # print(row['project'])
    sf_ticket = get_ticket_number_from_subproject(row['subproject'])
    combined = row['project'] + ':' + row['subproject']

    # print(f'sf_ticket: {sf_ticket}, combined: {combined}')

    return TICKET_LOOKUP[sf_ticket] if sf_ticket else TICKET_LOOKUP[combined]


def preprocess_data():
    df = pd.read_csv('time-entries.csv')

    # print(df.subproject.unique().tolist())
    # print(list(map(get_ticket_number_from_subproject, df.subproject.unique().tolist())))

    ticket_numbers = list(filter(lambda sp: sp is not None and sp.startswith('LT'), map(get_ticket_number_from_subproject, df.subproject.unique().tolist())))

    ticket_ids = ticket_lookup(ticket_numbers)

    TICKET_LOOKUP.update(ticket_ids)

    # print(TICKET_LOOKUP)
    # print(list(df.groupby(['date', 'project', 'subproject'])['subproject']))

    aggregation = pd.concat([df.groupby(['date', 'project', 'subproject', 'effortType'])['subject'].apply(';'.join), df.groupby(['date', 'project', 'subproject', 'effortType']).sum()], axis=1).reset_index()

    aggregation['comb-project-subproject'] = aggregation['project'] + ':' + aggregation['subproject'] + ':::' + aggregation['subject']

    # print(aggregation)


    # aggregation = pd.concat([df.groupby(['date', 'project', 'subproject'])['subject'].apply(
    #     ';'.join), df.groupby(['date', 'project'])['subproject'].apply(
    #     ';'.join), df.groupby(['date', 'project']).sum()], axis=1).reset_index()
    
    rcgna_aggregation = aggregation.loc[aggregation['project'] == 'RCGNA']
    other_aggregation = aggregation.loc[aggregation['project'] != 'RCGNA']


    rcgna_df = pd.DataFrame(RCGNA_TICKETS)

    rcgna_aggregation['key'] = 0
    rcgna_df['key'] = 0

    rcgna_join = rcgna_aggregation.merge(rcgna_df, on='key', how='outer')
    # print(rcgna_join)

    rcgna_join = rcgna_join.rename(columns={0: 'ticket'})

    other_aggregation['ticket'] = other_aggregation.apply(
        get_ticket_for_row, axis=1)

    # rcgna_join.to_csv('rcgna.csv')
    # other_aggregation.to_csv('other.csv')

    both = pd.concat([rcgna_join, other_aggregation])

    both = both.rename(
        columns={'subject': 'Subject', 'comb-project-subproject': 'Description', 'time': 'Hours Worked'})

    both = both.drop(columns=['project', 'subproject', 'key'])

    print(both)

    # raise Exception('halt')
    both.to_csv('time-entries-preprocess-output.csv', index=False)


def execute():
    print("Preprocessing...")
    preprocess_data()
    print("Complete!!")


execute()
