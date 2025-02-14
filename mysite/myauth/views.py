from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('recipeapp:recipe_index')  # Указываем, куда редиректить после входа

    def get_success_url(self):
        # Получаем параметр `next` из запроса
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        return next_url or self.next_page


# Вью для регистрации
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipeapp:recipe_index')  # Перенаправление после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'myauth/signup.html', {'form': form})
