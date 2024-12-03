from django.shortcuts import render
from django.views import View
from .models import (
    Categoria, Marca, Produto, Cliente, Venda, ItemVenda, Pagamento,
    EnderecoEntrega, Avaliacao, Comentario, Cupom, Carrinho, 
    ItemCarrinho, Desejo, ItemDesejo, Notificacao, Log
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


###############################################################################
# CONTROLADORES DA APLICAÇÃO (RESPONSÁVEIS POR GERENCIAR AS REQUISIÇÕES HTTP) #
###############################################################################


class CustomLoginView(View):
    page = 'pages/login.html'

    def get(self, request):
        return render(request, self.page)
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'pages/index.html')
        else:
            return render(request, self.page, {'error': 'E-mail ou senha incorretos'})
        

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'pages/index.html')
    

class RegisterView(View):
    page = 'pages/register.html'

    def get(self, request):
        return render(request, self.page)
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return render(request, 'pages/login.html')
        else:
            return render(request, self.page, {'error': 'Senhas não conferem'})



class IndexView(View):
    page = 'pages/index.html'

    def get(self, request):
        return render(request, self.page)
    
    def post(self, request):
        pass


class ProductDetailView(View):
    page = 'pages/product-detail.html'

    def get(self, request):
        return render(request, self.page)
    
    def post(self, request):
        pass


class CartView(View):
    page = 'pages/sacola.html'

    def get(self, request):
        return render(request, self.page)
    
    def post(self, request):
        pass