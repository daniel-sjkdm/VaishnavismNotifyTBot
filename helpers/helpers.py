from markdown2 import markdown
from PIL import Image
import imgkit
import pdfkit
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


def html_to_pdf(text, write=False):
    html_text = markdown(text, extras=["cuddled-lists"])
    if not write:
        pdf_bytes = pdfkit.from_string(html_text, output_path=False, options={'quiet': ''})
        return io.BufferedReader(io.BytesIO(pdf_bytes))
    else:
        file_name = "".join(map(str, [random.randint(0,100) for n in range(10)])) + ".pdf"
        pdfkit.from_string(html_text, output_path=f"tmp/{file_name}")
        return os.path.abspath(f"tmp/{file_name}")

def html_to_pdf_v2(text):
    md_text = markdown(text, extras=["cuddled-lists"])
    pdffile = io.BytesIO()
    pisa.CreatePDF(md_text, dest=pdffile)
    print("---  @@@ ---")
    print(pdffile.getvalue())
    print(io.BufferedReader(pdffile.getvalue())
    return io.BufferedReader(pdffile.getvalue())
