"""Integrate GatorGrouper with Google Sheets."""

import csv
import math
import logging
import gspread
from genetic_algorithm import Student
from oauth2client.service_account import ServiceAccountCredentials
import config
import pandas as pd
import os.path


EMAIL_COL = None
PREFERENCES_COL = None
SKILLS_COLS = set()

STUDENTS = None
GROUPING_SIZE = None

def get(group_size):
    """Retrieve data from Google Sheets and write to a CSV file."""

    global EMAIL_COL
    global PREFERENCES_COL
    global SKILLS_COLS

    if not os.path.isfile(config.WORKBOOK_CSV):
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
        for entry in records:
            formatted_entry = list()
            for index, (question, response) in enumerate(entry.items()):
                if question == 'Email Address':
                    EMAIL_COL = index - 1  # subtracting one because timestamp column not collected
                    formatted_entry.append(response)
                elif "prefer" in question:
                    PREFERENCES_COL = index - 1
                    formatted_entry.append(response)
                elif "skill" in question:
                    SKILLS_COLS.add(index - 1)
                    formatted_entry.append(response)
            formatted_records.append(formatted_entry)

        logging.debug("Writing formatted records to " + config.WORKBOOK_CSV + "...")
        with open(config.WORKBOOK_CSV, 'w') as output:
            writer = csv.writer(output, quoting=csv.QUOTE_ALL)
            for item in formatted_records:
                writer.writerow(item)

    global STUDENTS
    global GROUPING_SIZE

    EMAIL_COL = 0
    PREFERENCES_COL = 1
    SKILLS_COLS = [2, 3, 4, 5, 6]

    DATA = pd.read_csv(config.WORKBOOK_CSV, header=None)

    EMAILS = DATA.iloc[:, EMAIL_COL]

    STUDENTS = list()
    for current_row, email in enumerate(EMAILS):
        skills = list()
        for skill_col in SKILLS_COLS:
            skills.append(DATA.iat[current_row, skill_col])
        preferences_str = DATA.iat[current_row, PREFERENCES_COL]

        if isinstance(preferences_str, float) and math.isnan(preferences_str):
            preferences = []
        else:
            preferences = preferences_str.replace(" ", "").split(",")

        STUDENTS.append(Student(email, skills, preferences))

    for student in STUDENTS:
        print(str(student) + "\n")

    GROUPING_SIZE = math.floor(len(STUDENTS) / group_size)
