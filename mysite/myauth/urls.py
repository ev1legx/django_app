from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    CustomLogoutView, SignUpView, ReadCookiesView, SetCookiesView,
    ReadSessionView, SetSessionView,
    UsersListView, UserProfileDetailView,
    AboutMeView, EditUserProfileView
)

urlpatterns = [
    # Вход в систему, с указанием кастомного шаблона
    path('login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),

    # Выход из системы с использованием своего класса
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Регистрация
    path('signup/', SignUpView.as_view(), name='signup'),

    # Работа с cookie
    path('cookies/read/', ReadCookiesView.as_view(), name='read_cookies'),
    path('cookies/set/', SetCookiesView.as_view(), name='set_cookies'),

    # Работа с сессиями
    path('session/read/', ReadSessionView.as_view(), name='read_session'),
    path('session/set/', SetSessionView.as_view(), name='set_session'),

    # Список пользователей
    path('users/', UsersListView.as_view(), name='users_list'),

    # Детали профиля пользователя
    path('users/<int:user_id>/', UserProfileDetailView.as_view(), name='user_profile_detail'),

    # "О себе" - редактирование своего профиля (аватар)
    path('about-me/', AboutMeView.as_view(), name='about_me'),

    # Редактирование чужого профиля (аватар)
    path('users/<int:user_id>/edit/', EditUserProfileView.as_view(), name='edit_user_profile'),
]
