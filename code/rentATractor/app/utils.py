
from django.template.loader import get_template
from weasyprint import HTML

def printTicket():
    template = get_template("confirmacion.html")
    context = {"name": "Irene"}
    html_template = template.render(context)
    HTML(string=html_template).write_pdf(target="ticket.pdf")

printTicket()
    
