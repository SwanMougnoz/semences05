from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from s5appadherant.forms import LoginForm


class LoginView(TemplateView):

    template_name = "s5appadherant/login.html"

    def get(self, request, *args, **kwargs):
        form = kwargs.get('form', LoginForm())
        message = kwargs.get('message', None)

        return self.render_to_response({
            'form': form,
            'message': message
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("s5vitrine.contact_envoye_view")
            else:
                message = "L'email ou le mot de passe est incorrect"
                return self.get(request, form=form, message=message)

        return self.get(request, form=form)
