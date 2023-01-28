from .forms import CreateCompanyForm


def create_company_form(request):
    return {'create_company_form': CreateCompanyForm}