from django.shortcuts import render
from django.template.response import TemplateResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login
from django.shortcuts import redirect

class RegisterFormView(FormView):
     form_class = UserCreationForm

     # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
     # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
     success_url = "/"

     # Шаблон, который будет использоваться при отображении представления.
     template_name =  "web/register.html"

     def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView (FormView):
        #request,
        #template_name = 'web/main.html'):

    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "web/main.html"

    success_url = "/client"

    def render_to_response(self, context):

        if self.request.user.is_authenticated():
            return redirect("/client")

        return super(LoginFormView, self).render_to_response(context)

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

    """
    auth = False
    if request.user.is_authenticated():
        auth = True
        redirect_to = "/client"
        return HttpResponseRedirect(redirect_to)

    context = {
        'user':request.user,
        'auth':auth
    }


    return TemplateResponse(request, template_name, context)
    """

def client (  request,
        template_name = 'web/client.html'):

    username = request.user.username
    userId = request.user.id

    context = {
        "username":username,
        "userId":userId
    }

    return TemplateResponse(request, template_name, context)