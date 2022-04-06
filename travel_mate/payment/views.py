from django.shortcuts import redirect
from django.views.generic.base import TemplateView,View
from django.db.models import Count
import user.models as usr_model

class List(TemplateView):
    template_name="payment.html"
    
    def get(self, request, *args, **kwargs):
        context = {}
        if(request.user.is_authenticated):
            payment = usr_model.Payment.objects.select_related('content_idx').filter(name=request.user.name).values('content_idx_id', 'content_idx__name', 'content_idx__fee', 'content_idx__user_name')
            context['data'] = []
            for i in payment:
                content = usr_model.Content.objects.filter(idx=i['content_idx_id']).annotate(total=Count('payment'))
                i['pay'] = int(round(i['content_idx__fee']/content[0].total,-2))
                context['data'].append(i)
            return self.render_to_response(context)
        else:
            return redirect(to="/")