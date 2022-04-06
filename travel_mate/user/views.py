from django.views.generic.base import TemplateView,View
from django.shortcuts import redirect
from django.contrib.auth import login, logout
import user.models as usr_model

class Login(TemplateView):
    template_name="signin.html"
    
    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect(to="/content")
        context = {}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect(to="/content")
        context = {}
        name = request.POST['name']
        try:
            user = usr_model.User.objects.get(name=name)
            if user is not None:
                login(request, user)
                return redirect(to="/content")
        except:
            pass
        return self.render_to_response(context)

class Logout(View):    
    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            logout(request)
            return redirect(to="/")
        else:
            return redirect(to="/")
