
from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML

def printTicket():
    template = get_template("factura.html")
    context = {
        "pedido": "Irene",
        "icon": '{}{}'.format(settings.MEDIA_URL, 'logo.png')
        }
    html_template = template.render(context)

    HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target="factura.pdf")

printTicket()
    
