#!/usr/bin/python3

import requests
import json
from argparse import ArgumentParser
import re
# Describing Command-Line Arguments
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
parser.add_argument("-p", dest="period", required=True,
                    help='billing period. Available values: BillingMonthToDate, MonthToDate, TheLastBillingMonth, TheLastMonth, TheLastWeek, TheLastYear, WeekToDate, YearToDate', metavar="PERIOD")
parser.add_argument("-o", dest="output", required=True,
                    help='output file name, e.g. excel.xlsx', metavar="OUTPUT_FILE")

args = parser.parse_args()

# Making access token request
a_url = "https://login.microsoftonline.com/%s/oauth2/token" % args.tenant
a_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

a = requests.post(a_url, headers=a_headers, data={'grant_type': 'client_credentials','resource': 'https://management.azure.com/','client_secret': args.secret,'client_id': args.app_id}).json()

b = a["token_type"]
c = a["access_token"]
d = f'{b} {c}'

# Making resource group usage request
b_url = "https://management.azure.com/subscriptions/%s/providers/Microsoft.CostManagement/query?api-version=2019-01-01" % args.subscription
b_headers = {'Content-Type': 'application/json', 'Authorization': d}
data = '''{
    "type": "Usage",
    "timeframe": "%s",
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
}''' % args.period

resp = requests.post(b_url, headers=b_headers, data=data).json()

mylist = resp['properties']['rows']

l=[]

for element in args.groups:
    for idx, value in enumerate(mylist):
        if re.search(element, str(value)):
            l.append(value)

r=[]
for idx, val in enumerate(l):
    r.append(val[2])

p=[]
for idx, val in enumerate(l):
    p.append(val[0])

d=[]
for idx, val in enumerate(l):
    d.append(val[1])

t=[]
for idx, val in enumerate(mylist):
    t.append(val[0])

s=(sum(t))

from collections import OrderedDict

e = list(OrderedDict.fromkeys(d))

import xlsxwriter
from datetime import datetime

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(args.output)
worksheet = workbook.add_worksheet("Stryker-Robotics-Stage1")

date_format = workbook.add_format({'num_format': 'mmmm', 'align': 'center'})
money_format = workbook.add_format({'num_format': '$0,#.00', 'align': 'center'})
group_format = workbook.add_format({'align': 'center'})

worksheet.set_column('B1:K4', 40)

row = 1
col = 1
bold = workbook.add_format({'bold': 1, 'align': 'center'})

for item in r:
    worksheet.write(row, col, item, group_format)
    col += 1

col = 1
for i in p:
    worksheet.write(row + 1, col, i, money_format)
    col += 1

col = 0
for date in e:
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    worksheet.write(row + 1, col, date, date_format)
    row += 1

worksheet.merge_range('A1:A2', 'Date', bold)
worksheet.merge_range('B1:K1', 'Resource Group', bold)

worksheet.write(row + 1, 0, 'Total', bold)
worksheet.write(row + 2, col, s, money_format)
worksheet.merge_range('B4:C4', '=SUM(B3:C3)', money_format)
worksheet.merge_range('D4:E4', '=SUM(D3:E3)', money_format)
worksheet.merge_range('F4:G4', '=SUM(F3:G3)', money_format)
worksheet.merge_range('H4:I4', '=SUM(H3:I3)', money_format)
worksheet.merge_range('J4:K4', '=SUM(J3:K3)', money_format)

workbook.close()
