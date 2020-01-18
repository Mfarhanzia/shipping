from .forms import EmailListForm


def email_form(request):
    form = EmailListForm()
    return {"subscribe_form":form}