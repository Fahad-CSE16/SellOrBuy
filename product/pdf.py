from io import BytesIO
from django.shortcuts import render , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View

from xhtml2pdf import pisa

from .models import Order

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def admin_order_pdf( request,order_id):
    template = get_template('order_pdf.html')
    order=get_object_or_404(Order,pk=order_id)

    context = {
        'order':order
    }
    html = template.render(context)
    pdf = render_to_pdf('order_pdf.html', context)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "inline; filename=%s.pdf" % order_id
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
