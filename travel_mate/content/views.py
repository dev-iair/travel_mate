from django.shortcuts import redirect
from django.views.generic.base import TemplateView,View
from django.db.models import Count
import user.models as usr_model

class List(TemplateView):
    template_name="list.html"
    
    def get(self, request, *args, **kwargs):
        context = {}
        if(request.user.is_authenticated):
            content = usr_model.Content.objects.all()
            contents = content.values('name','fee','idx','user_name').annotate(total=Count('payment'))
            context['data'] = []
            for i in contents:
                i['pay'] = int(round(i['fee']/i['total'],-2))
                context['data'].append(i)
            return self.render_to_response(context)
        else:
            return redirect(to="/")

    def post(self, request, *args, **kwargs):
        context = {}
        if(request.user.is_authenticated):
            return self.render_to_response(context)
        else:
            return redirect(to="/")

class Register(TemplateView):
    template_name="register.html"
    
    def get(self, request, *args, **kwargs):
        context = {}
        if(request.user.is_authenticated):
            users = usr_model.User.objects.all().values('name')
            context['user'] = []
            for i in users:
                context['user'].append(i['name'])
            return self.render_to_response(context)
        else:
            return redirect(to="/")

    def post(self, request, *args, **kwargs):
        context = {}
        if(request.user.is_authenticated):
            name = request.POST['name']
            fee = request.POST['fee']
            party_list = request.POST.getlist('nameCheck')
            party_list.append(request.user.name)
            new_content = usr_model.Content()
            new_content.name = name
            new_content.fee = fee
            new_content.user_name = request.user.name
            new_content.save()
            new_party_list = [usr_model.Payment(content_idx_id=new_content.idx, name_id=name) for name in party_list]
            usr_model.Payment.objects.bulk_create(new_party_list)
            return redirect(to="/content")
        else:
            return redirect(to="/")

class Delete(View):

    def post(self, request, *args, **kwargs):
        context = {}
        if(request.user.is_authenticated):
            cont_idx = request.POST['idx']
            del_cont = usr_model.Content.objects.get(idx=cont_idx)
            del_cont.delete()
            return redirect(to="/content")
        else:
            return redirect(to="/")