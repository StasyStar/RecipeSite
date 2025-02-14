from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from myauth import views  # Убедитесь, что views импортированы правильно

app_name = 'myauth'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Страница входа
    path('signup/', views.signup, name='signup'),  # Страница регистрации
    path('logout/', LogoutView.as_view(next_page='/recipe/'), name='logout'),  # Страница выхода

    # Стандартные аутентификационные URL Django (для пароля и т.п.)
    path('', include('django.contrib.auth.urls')),
]


