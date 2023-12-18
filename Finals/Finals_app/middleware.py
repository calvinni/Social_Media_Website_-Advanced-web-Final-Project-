from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from Finals_app.models import *
import time

class SessiontimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_view(self, request, view_func, view_args, view_kwargs): 
        if 'member_id' in request.session:
            expires_time = request.session['session_time_expiry']
            timeleft = expires_time - time.time()
            # print(expires_time)
            if timeleft < 10:
                Users.objects.filter(id=request.session['member_id']).update(is_online=False)
                del request.session['member_id']
                request.session.clear_expired()
                messages.success(request, 'session timed out, Please login')
                return HttpResponseRedirect(reverse('index'))
