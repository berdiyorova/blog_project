from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserRegisterForm, UserEditForm


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.info(request, "Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('login')

        return render(request, 'users/register.html', {'form': form})



class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')

        return render(request, 'users/login.html', {'form': form})



class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "Siz muvaffaqiyatli saytdan chiqdingiz.")
        return redirect('home_page')



class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})



class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        user_edit_form = UserEditForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'form': user_edit_form})

    def post(self, request):
        user_edit_form = UserEditForm(instance=request.user,
                                          data=request.POST,
                                          files=request.FILES
                                          )

        if user_edit_form.is_valid():
            user_edit_form.save()
            messages.success(request, "Profilingiz muvaffaqiyatli tahrirlandi.")
            return redirect('profile')

        return render(request, 'users/profile_edit.html', {'form': user_edit_form})
