from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



# Класс для выхода из системы с перенаправлением на страницу логина
class CustomLogoutView(LogoutView):
    next_page = '/accounts/login/'  # Адрес перенаправления после logout


# Класс регистрации пользователя
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('shop_index')

    def form_valid(self, form):
        # При успешной регистрации автоматически логиним пользователя
        response = super().form_valid(form)
        user = self.object
        from django.contrib.auth import login
        login(self.request, user)
        return response


# Класс для чтения cookie
class ReadCookiesView(View):
    def get(self, request, *args, **kwargs):
        value = request.COOKIES.get('my_cookie', 'Значение по умолчанию')
        return HttpResponse(f'Значение cookie: {value}')


# Класс для установки cookie
class SetCookiesView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse("Cookie установлено")
        response.set_cookie('my_cookie', 'value123')
        return response


# Класс для чтения сессии
class ReadSessionView(View):
    def get(self, request, *args, **kwargs):
        value = request.session.get('my_session', 'Значение по умолчанию')
        return HttpResponse(f'Значение сессии: {value}')


# Класс для установки сессии
class SetSessionView(View):
    def get(self, request, *args, **kwargs):
        request.session['my_session'] = 'какое-то значение'
        return HttpResponse("Сессия установлена")


# Класс для отображения списка пользователей
class UsersListView(LoginRequiredMixin, ListView):
    model = User  # Модель User
    template_name = 'myAuth/users_list.html'  # Шаблон списка пользователей
    context_object_name = 'users'  # В шаблоне доступны через переменную users


# Класс для отображения деталей профиля пользователя
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'myAuth/user_profile_detail.html'

    def get_object(self, queryset=None):
        # Получаем профиль пользователя по user_id URL
        user_id = self.kwargs.get('user_id')
        user_obj = get_object_or_404(User, pk=user_id)
        return user_obj.profile

    def get_context_data(self, **kwargs):
        # Передаём в шаблон можно ли редактировать профиль (владелец или staff)
        context = super().get_context_data(**kwargs)
        user_obj = self.object.user
        context['can_edit'] = self.request.user.is_staff or (self.request.user == user_obj)
        return context


# Класс для редактирования своего профиля (только аватар)
class AboutMeView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ('avatar',)  # Менять разрешено только avatar
    template_name = 'myAuth/about-me.html'
    success_url = reverse_lazy('about_me')

    def get_object(self, queryset=None):
        # Возвращаем профиль текущего пользователя
        return Profile.objects.get(user=self.request.user)


# Класс для редактирования чужого профиля (с проверкой прав, менять только аватар)
class EditUserProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ('avatar',)
    template_name = 'myAuth/edit_user_profile.html'
    success_url = reverse_lazy('users_list')

    def get_object(self, queryset=None):
        # Получаем профиль пользователя из URL
        user_id = self.kwargs.get('user_id')
        user_obj = get_object_or_404(User, pk=user_id)
        return user_obj.profile

    def test_func(self):
        # Проверка: редактировать можно если сотрудник (staff) или владелец
        user_id = self.kwargs.get('user_id')
        return self.request.user.is_staff or (self.request.user.id == user_id)
