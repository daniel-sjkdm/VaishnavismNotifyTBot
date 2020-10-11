from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from io import BufferedReader, BytesIO
from settings import BASE_DIR
import os.path
import pdfkit 


template_path = os.path.join(BASE_DIR, "beautify/templates")

env = Environment(
    loader=FileSystemLoader(template_path),
    autoescape=select_autoescape(["html", "xml"]),
)


config = pdfkit.configuration(wxhtmltopdf=os.path.join(BASE_DIR, "bin/wwkhtmltopdf"))


def beautify_to_pdf(data, kind):
    template = env.get_template("ekadasi_events.html")
    css = [
        os.path.join(BASE_DIR, "beautify/static/css/bootstrap.css")   
    ]

    if kind == "ekadasi":
        template = env.get_template("ekadasi_events.html")
        css.append(os.path.join(BASE_DIR, "beautify/static/css/ekadasi_events.css"))

    elif kind == "iskcon_events":
        template = env.get_template("iskcon_events.html")
        css.append(os.path.join(BASE_DIR, "beautify/static/css/iskcon_events.css"))

    html = template.render(
        events=data["events"],
        year=data["year"],
        month=data["month"]
    )

    pdffile_bytes = BytesIO(pdfkit.from_string(html, output_path=False, css=css, configuration=config))
    return BufferedReader(BytesIO(pdffile_bytes.getvalue()))
