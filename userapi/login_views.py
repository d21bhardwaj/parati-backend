from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import *
from django.contrib.auth import get_user_model
User = get_user_model()
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
           #Add mail here
            return redirect('user')
    else:
        form = SignUpForm()
    return render(request, 'login/signup.html',{'form': form , 'header':'Sign Up'})

def activate_account(request,token):
    token = decrypt_val(token)
    iden = int(token.split(";")[0])
    usr = User.objects.filter(id=iden).first()
    usr.email_verified = True
    usr.save()
    return redirect("usr")

def mail_send():
    mail = request.POST['profile-0-email']
    usr = Profile.objects.filter(user_id=request.user.id).first()
    template = get_template('email_ver.txt')
    context = {
    "name" : usr.name,
    "link": "https://parti.in/activate_account/"+encrypt_val(str(usr.id)+";"+usr.name),
    }
    content = template.render(context)
    email = EmailMessage(
        "Email Verification",
        content,
        "Parati" +'',
        [mail],
        headers = {'Reply-To': 'project.pinetown@gmail.com' }
    )
    email.send()