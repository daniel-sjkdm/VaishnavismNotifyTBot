from markdown2 import markdown
import re
import io
import random
import os
from xhtml2pdf import pisa


MONTH_TO_NUMBER = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


NUMBER_TO_MONTH = dict(map(lambda x, y: (y, x), MONTH_TO_NUMBER.keys(), MONTH_TO_NUMBER.values()))


DAY_TO_NUMBER = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}


NUMBER_TO_DAY = dict(map(lambda x, y: (y, x), DAY_TO_NUMBER.keys(), DAY_TO_NUMBER.values()))

DATE_PATTERN = re.compile("((1?[012]|[1-9])(-\d{4})?|(\d{4})(-(1?[012]|[1-9]))?)")


def html_to_pdf_v2(text):
    md_text = markdown(text, extras=["cuddled-lists"])
    pdffile = io.BytesIO()
    pisa.CreatePDF(md_text, dest=pdffile)
    return io.BufferedReader(io.BytesIO(pdffile.getvalue()))


def events_to_dict(events, kind):
    events_dict = []
    if kind == "ekadasi":
        for event in events:
            name = event[7]
            year, month, _ = event[3].strftime("%Y-%m-%d").split("-")
            day = NUMBER_TO_DAY[int(event[3].weekday() + 1)]

            starts = event[4].strftime("%H:%M") 
            ends = event[5].strftime("%H:%M")
            body = event[8]

            date = f"{NUMBER_TO_MONTH[int(month)]} {day}, {year}, {day}" 

            events_dict.append({
                "title": name,
                "date": date,
                "starts": starts,
                "ends": ends,
                "body": body
            })
    
    elif kind == "iskcon":
        for event in events:
            name = event[1]
            year, month, _ = event[3].strftime("%Y-%m-%d").split("-")
            day = NUMBER_TO_DAY[int(event[3].weekday() + 1)] 

            date = f"{NUMBER_TO_MONTH[int(month)]} {day}, {year}, {day}" 

            events_dict.append({
                "name": name, 
                "date": date
            })

    return events_dict