from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()

@register.filter
def bootstrap_table(form):
    template = get_template("bootstrap/table.html")
    context = Context({'form': form})
    return template.render(context)


@register.filter
def bootstrap_form(form):
    template = get_template("bootstrap/form.html")
    context = Context({'form': form})
    return template.render(context)
@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"
