from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from core.forms import LoginForm, UserForm

def index(request):
    return render_to_response('index.html', {
    }, context_instance=RequestContext(request))

def login_user(request, template='index.html', redirect_url=None):

    def handle_login_error(login_error):
        form = LoginForm()
        return render_to_response(template, {
            'login_error' : login_error,
            'login_form' : form,
        }, context_instance=RequestContext(request))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            redirect_url = redirect_url or form.cleaned_data.get('redirect_url')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Redirect to a success page.
                    login(request, user)
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    else:
                        return render_to_response(template, {
                            'login_succeeded': True
                        }, context_instance=RequestContext(request))
                else:
                    # Return a 'disabled account' error message
                    error = u'Account disabled'
            else:
                # Return an 'invalid login' error message.
                error = u'Invalid login'
        else: 
            error = u'Login form is invalid'

        return handle_login_error(error)

    else:
        form = LoginForm() # An unbound form
        form.fields['redirect_url'].initial = request.GET.get('next', '/')
        return render_to_response(template, {
            'login_error': "You must first login",
            'form': form
        }, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect('/')
    return response

def create_account(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(username=user.username, password=request.POST['password'])            
            login(request, authenticated_user)
            return render_to_response('index.html', {
                    'login_succeeded': True
                    }, context_instance=RequestContext(request))        
        else:
            return render_to_response(
                'create_account.html',
                {'form': form},
                context_instance=RequestContext(request)
                )
    else:
        form = UserForm()
        return render_to_response(
            'create_account.html',
            {'form': form},
            context_instance=RequestContext(request)
            )
