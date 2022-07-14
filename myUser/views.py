from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserSignUpForm,EditStatusForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import Video,pythonCode
import requests
import csv
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


JDOODLE_INFO = {
    'clientId' : '955c02a67dab8632da1bfda6b53d4fd3',
    'clientSecret' : '4f50bf0ab404ca19efaae76d33ce378f90f569cf16e72fe26dc54939087b8f1',
    'url' : 'https://api.jdoodle.com/v1/execute'
}

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('myUser-login')
    else:
        form = UserSignUpForm()
    
    return render(request, 'signup.html', {'form': form, 'title': 'Sign Up'})

@login_required
def course(request, index=1):
    context = {
        'main_video': Video.objects.all()[index-1],
        'videos': Video.objects.all(),
        'index': index,
        'title': 'Course ' + str(index),
        'form2' : False,
    }
    if request.method == "POST":
        if(request.POST.get('codearea',None) != None):
            codeareadata = request.POST['codearea']

            url = JDOODLE_INFO['url']
            myobj = {
                'clientId': JDOODLE_INFO['clientId'],
                'clientSecret': JDOODLE_INFO['clientSecret'],
                'script': codeareadata,
                'stdin': '',
                'language': 'python3',
                'versionIndex': 0
            }

            output_json = requests.post(url, json=myobj).json()
            output = output_json['output']
            output = output.replace('Jdoodle', 'Main').replace('jdoodle', 'main')
            
            if(not codeareadata.isspace() and len(codeareadata)):
                my_code = pythonCode(user=request.user,codearea=codeareadata,output=output,session_key=request.session.session_key)
                my_code.save()
                context['form2_val'] = EditStatusForm(instance=my_code)
                context['form2'] = True
               

            context['code'] = codeareadata
            context['output'] = output
            context['my_code'] = my_code
            return render(request, 'home.html', context=context)
        else:
            my_code = pythonCode.objects.filter(user=request.user).first()
            form = EditStatusForm(request.POST,instance=my_code)
            if form.is_valid():
                form.save()
            context['code'] = my_code.codearea
            context['form2'] = True
            context['form2_val'] = EditStatusForm(instance=my_code)
            context['output'] = my_code.output
            context['my_code'] = my_code
            return render(request, 'home.html', context=context)

    else:
        return render(request, 'home.html', context=context)

@login_required
def listcodes(request):
    context = {
        'title' : 'Submissions of ' + str(request.user.username),
        'codes' : pythonCode.objects.filter(user=request.user)
    }
    return render(request,'list_codes.html',context=context)


@login_required
def detailcodes(request,index=1):
    code = pythonCode.objects.filter(user=request.user)[index-1]
    form = EditStatusForm(instance=code)
    if request.method == 'POST':
        form = EditStatusForm(request.POST,instance=code)
        if form.is_valid():
            form.save()
            return redirect('/list_codes/')
    
    
    context = {
        'title' : str(code),
        'code'  : code,
        'form' : form
    }
    return render(request,'detail_code.html',context)

@login_required
def download_data(request):
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        writer.writerow(['Username','Session Key', 'Code', 'Output','Date','Time','Done','Feedback'])
        for code in pythonCode.objects.all():
            column = [code.user.username,code.session_key,code.codearea,code.output,code.date,code.time,code.Done,code.Feedback]
            writer.writerow(column)
        
        response['Content-Disposition'] = 'attachment; filename="codes.csv"'
        return response
    else:
        context = {
        'title' : 'Submissions of ' + str(request.user.username),
        'codes' : pythonCode.objects.filter(user=request.user)
        }   
        return render(request,'list_codes.html',context=context)

class MyLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'video' : Video.objects.all().first()
        })
        return context