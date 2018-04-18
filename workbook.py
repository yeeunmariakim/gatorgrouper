"""Integrate GatorGrouper with Google Sheets."""

import csv
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

email_index = None
preferences_index = None
skills_indices = list()


def get():
    """Retrieve data from Google Sheets and write to a CSV file."""

    logging.info(
        "Authenticating to Google Sheets...")

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    client = gspread.authorize(creds)

    logging.info("Opening spreadsheet...")
    sheet = client.open(config.WORKBOOK).sheet1

    logging.info("Extracting data from spreadsheet...")
    records = sheet.get_all_records()

    formatted_records = list()
    for index, entry in enumerate(records):
        formatted_entry = list()
        for question, response in entry.items():
            if question == 'Email Address':
                email_index = index
                formatted_entry.append(response)
            elif "prefer" in question:
                preferences_index = index
                formatted_entry.append(response)
            elif "skill" in question:
                skills_indices.append(index)
                formatted_entry.append(response)
        formatted_records.append(formatted_entry)

    logging.debug("Writing formatted records to " + config.WORKBOOK_CSV + "...")
    with open(config.WORKBOOK_CSV, 'w') as output:
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        for item in formatted_records:
            writer.writerow(item)
