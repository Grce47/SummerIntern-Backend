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


JDOODLE_INFO = {    #JDoodle Dictionary
    'clientId' : '955c02a67dab8632da1bfda6b53d4fd3',
    'clientSecret' : '4f50bf0ab404ca19efaae76d33ce378f90f569cf16e72fe26dc54939087b8f1',
    'url' : 'https://api.jdoodle.com/v1/execute'
}

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST) # Use Django's default password change form
        if form.is_valid():
            user = form.save()                      # save the user
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')    # and send a message
            return redirect('change_password') 
        else:
            messages.error(request, 'Please correct the error below.') # When the form is not valid
    else:
        form = PasswordChangeForm(request.user)     #in case of GET request, form is produced
    return render(request, 'change_password.html', {
        'form': form
    })

def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST) #use UserSignUpForm from forms.py
        if form.is_valid():                 # if form is valid
            form.save()                     # save the user
            username = form.cleaned_data.get('username')   #get username     
            messages.success(request,f'Account created for {username}!')    #print this message
            return redirect('myUser-login')     # go to login page
    else:
        form = UserSignUpForm()     #in case of GET request, send this form
    
    return render(request, 'signup.html', {'form': form, 'title': 'Sign Up'})

@login_required
def course(request, index=1):
    context = {
        'main_video': Video.objects.all()[index-1], #main video
        'videos': Video.objects.all(),              #all videos
        'index': index,                             #index passed into the function
        'title': 'Course ' + str(index),            #Custom title
        'form2' : False,                            #flag
    }
    if request.method == "POST":
        if(request.POST.get('codearea',None) != None):
            codeareadata = request.POST['codearea']     #running codes

            url = JDOODLE_INFO['url']                   #from the dictionary
            myobj = {
                'clientId': JDOODLE_INFO['clientId'],
                'clientSecret': JDOODLE_INFO['clientSecret'],
                'script': codeareadata,         #the code
                'stdin': '',
                'language': 'python3',
                'versionIndex': 0
            }

            output_json = requests.post(url, json=myobj).json()     #get the output json
            output = output_json['output']      #take the output
            output = output.replace('Jdoodle', 'Main').replace('jdoodle', 'main')      #change the strings so that Jdoodle does not show up everywhere
            
            if(not codeareadata.isspace() and len(codeareadata)):   #if code is not empty
                my_code = pythonCode(user=request.user,codearea=codeareadata,output=output,session_key=request.session.session_key)
                my_code.save()  #save the code
                context['form2_val'] = EditStatusForm(instance=my_code) #Done and feedback
                context['form2'] = True
               

            context['code'] = codeareadata
            context['output'] = output
            context['my_code'] = my_code
            return render(request, 'home.html', context=context)    #render with output and code
        else:
            my_code = pythonCode.objects.filter(user=request.user).first()  #get the first code
            form = EditStatusForm(request.POST,instance=my_code)    #show that code
            if form.is_valid():
                form.save()
            context['code'] = my_code.codearea
            context['form2'] = True
            context['form2_val'] = EditStatusForm(instance=my_code)
            context['output'] = my_code.output
            context['my_code'] = my_code
            return render(request, 'home.html', context=context)    #render with the code and the output of it

    else:
        return render(request, 'home.html', context=context)    #return with empty code and ouput fields

@login_required
def listcodes(request): # list all the codes by an user
    context = {
        'title' : 'Submissions of ' + str(request.user.username),
        'codes' : pythonCode.objects.filter(user=request.user)      #filter to get all required codes
    }
    return render(request,'list_codes.html',context=context)


@login_required
def detailcodes(request,index=1):   
    code = pythonCode.objects.filter(user=request.user)[index-1]    #get detail of the specific code
    form = EditStatusForm(instance=code)                            #feedback form and done check
    if request.method == 'POST':
        form = EditStatusForm(request.POST,instance=code)
        if form.is_valid():
            form.save()                                             #if form is valid save it and return to list of all codes
            return redirect('/list_codes/')
    
    
    context = {
        'title' : str(code),
        'code'  : code,
        'form' : form
    }
    return render(request,'detail_code.html',context)               #render detail_code.html with context upon GET request

@login_required
def download_data(request):
    if request.user.is_staff:                                       #only when they are stuff
        response = HttpResponse(content_type='text/csv')            #response will be a csv file

        writer = csv.writer(response)
        writer.writerow(['Username','Session Key', 'Code', 'Output','Date','Time','Done','Feedback'])   #columns to be written
        for code in pythonCode.objects.all():
            column = [code.user.username,code.session_key,code.codearea,code.output,code.date,code.time,code.Done,code.Feedback]    #what to be written in each column
            writer.writerow(column)
        
        response['Content-Disposition'] = 'attachment; filename="codes.csv"'
        return response     #return
    else:
        context = {
        'title' : 'Submissions of ' + str(request.user.username),
        'codes' : pythonCode.objects.filter(user=request.user)
        }   
        return render(request,'list_codes.html',context=context)    #if not staff then just show them list_codes

class MyLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'video' : Video.objects.all().first()
        })
        return context