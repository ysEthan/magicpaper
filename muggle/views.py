from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def index_view(request):
    return render(request, 'home_page.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"欢迎回来, {username}!")
                return redirect('muggle:index')
            else:
                messages.error(request, "用户名或密码错误。")
        else:
            messages.error(request, "用户名或密码错误。")
    else:
        form = AuthenticationForm()
    return render(request, 'muggle/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功！")
            return redirect('muggle:index')
        else:
            messages.error(request, "注册失败，请检查输入信息。")
    else:
        form = UserCreationForm()
    return render(request, 'muggle/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "您已成功退出登录。")
    return redirect('muggle:login')

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                subject_template_name='muggle/password_reset_subject.txt',
                email_template_name='muggle/password_reset_email.html',
            )
            messages.success(request, "密码重置邮件已发送，请检查您的邮箱。")
            return redirect('muggle:login')
    else:
        form = PasswordResetForm()
    return render(request, 'muggle/password_reset.html', {'form': form})
