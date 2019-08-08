#!/usr/bin/python3

import requests
import json

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-g", dest="groups", nargs='+', required=True,
                    help='resource groups for the billing', metavar="RESOURCE_GROUP")
parser.add_argument("-t", dest="tenant", required=True,
                    help='tenant_id of SP', metavar="TENANT_ID")
parser.add_argument("-id", dest="app_id", required=True,
                    help='app_id of SP', metavar="APP_ID")
parser.add_argument("-sub", dest="subscription", required=True,
                    help='subscription id', metavar="SUBSCRIPTION_ID")
parser.add_argument("-secret", dest="secret", required=True,
                    help='secret of SP', metavar="SECRET")

args = parser.parse_args()

a_url = "https://login.microsoftonline.com/%s/oauth2/token" % args.tenant
a_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

a = requests.post(a_url, headers=a_headers, data={'grant_type': 'client_credentials','resource': 'https://management.azure.com/','client_secret': args.secret,'client_id': args.app_id}).json()

b = a["token_type"]
c = a["access_token"]
d = f'{b} {c}'

b_url = "https://management.azure.com/subscriptions/%s/providers/Microsoft.CostManagement/query?api-version=2019-01-01" % args.subscription
b_headers = {'Content-Type': 'application/json', 'Authorization': d}
data = '''{
    "type": "Usage",
    "timeframe": "TheLastMonth",
    "dataset": {
        "granularity": "Monthly",
        "grouping": [
            {
                "type": "Dimension",
                "name": "ResourceGroup"
            }
        ],
        "aggregation": {
            "totalCost": {
                "name": "PreTaxCost",
                "function": "Sum"
            }
        }
    }
}'''

resp = requests.post(b_url, headers=b_headers, data=data).json()

mylist = resp['properties']['rows']

l=[]

for element in args.groups:
    for idx, value in enumerate(mylist):
        if element in value:
            l.append(value)


import xlsxwriter
from datetime import datetime

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('excel.xlsx')
worksheet = workbook.add_worksheet('My Subscription')

date_format = workbook.add_format({'num_format': 'mmmm'})
money_format = workbook.add_format({'num_format': '$0.00'})
worksheet.set_column(1, 1, 20)
worksheet.set_column(1, 2, 40)

options = {'style': 'Table Style Light 11',
           'columns': [{'header': 'Date'},
                       {'header': 'Resource Group'},
                       {'header': 'Cost'}
                       ]}

row = 1
col = 0

for price, date, rg, currency in (l):

    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    worksheet.write(row, col, date, date_format)
    worksheet.write(row, col + 1, rg)
    worksheet.write(row, col + 2, price, money_format)
    row += 1

worksheet.write(row, 0, 'Total')
worksheet.write(row, 2, '=SUM(C2:C14)')

worksheet.add_table('A1:C15', options)

workbook.close()
