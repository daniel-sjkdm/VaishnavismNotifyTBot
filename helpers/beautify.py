from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from xhtml import pisa
from io import BufferedReader, BytesIO


env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
    enable_async=True
)


def beautify_events(events, kind):
    if kind == "ekadasi":
        template = env.get_template("ekadasi_events.html")
    elif kind == "iskcon_events":
        template = env.get_template("iskcon_events.html")
    html = template.render(
        events = events
    )
    pdffile_bytes = BytesIO()
    pisa.CreatePDF(src=html, dest=pdffile_bytes)
    return BufferedReader(BytesIO(pddfile_bytes.getvalue()))
