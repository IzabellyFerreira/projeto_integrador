from django.shortcuts import render, redirect, get_object_or_404   
from django.views import View
from .models import (
    Categoria, Marca, Produto, CustomUser, Venda, ItemVenda, Pagamento,
    EnderecoEntrega, Avaliacao, Comentario, Cupom, Carrinho, 
    ItemCarrinho, Desejo, ItemDesejo, Notificacao, Log
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse


###############################################################################
# CONTROLADORES DA APLICAÇÃO (RESPONSÁVEIS POR GERENCIAR AS REQUISIÇÕES HTTP) #
###############################################################################


class CustomLoginView(View):
    page = 'pages/login.html'

    def get(self, request):
        return render(request, self.page)
    
    def post(self, request):
        username = request.POST.get('form-username')
        password = request.POST.get('form-password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, self.page, {'error': 'Usuário ou senha incorretos'})
        

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'pages/index.html')
    

class RegisterView(View):
    page = 'pages/register.html'

    def get(self, request):
        return render(request, self.page)
    
    def post(self, request):
        username = request.POST.get('form-username')
        email = request.POST.get('form-email')
        password = request.POST.get('form-password')
        confirm_password = request.POST.get('form-confirm-password')
        if password == confirm_password:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
        else:
            return render(request, self.page, {'error': 'Senhas não conferem'})



class IndexView(View):
    page = 'pages/index.html'

    def get(self, request):
        return render(request, self.page)
    
    def post(self, request):
        pass


class ProductDetailView(View):
    template_name = 'pages/product-detail.html'

    def get(self, request, slug):
        produto = get_object_or_404(Produto, slug=slug)
        avaliacoes = Avaliacao.objects.filter(produto=produto, ativo=True).order_by('-data')
        
        # Calcula porcentagem de avaliações positivas (4 ou 5 estrelas)
        total_avaliacoes = avaliacoes.count()
        avaliacoes_positivas = avaliacoes.filter(estrelas__gte=4).count()
        porcentagem_positivas = (avaliacoes_positivas / total_avaliacoes * 100) if total_avaliacoes > 0 else 0
        
        context = {
            'produto': produto,
            'avaliacoes': avaliacoes,
            'porcentagem_positivas': round(porcentagem_positivas)
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, slug):
        produto = get_object_or_404(Produto, slug=slug)
        estrelas = int(request.POST.get('estrelas'))
        comentario_texto = request.POST.get('comentario')
        cliente = request.user

        avaliacao = Avaliacao.objects.create(
            produto=produto,
            cliente=cliente,
            estrelas=estrelas,
            ativo=True
        )
        Comentario.objects.create(
            avaliacao=avaliacao,
            texto=comentario_texto
        )
        return redirect('product-detail', slug=slug)


class CartView(View, LoginRequiredMixin):
    template_name = 'pages/sacola.html'

    def get(self, request):
        carrinho, created = Carrinho.objects.get_or_create(cliente=request.user)
        carrinho_items = ItemCarrinho.objects.filter(carrinho=carrinho)
        context = {'carrinho_items': carrinho_items}
        return render(request, self.template_name, context)

    def post(self, request):
        pass  # Lógica para atualizar quantidades, se necessário


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__cliente=request.user)
    item.delete()
    return redirect('cart')


@login_required
def finalize_purchase(request):
    carrinho = get_object_or_404(Carrinho, cliente=request.user)
    carrinho.itemcarrinho_set.all().delete()
    return redirect('cart')


@login_required
def add_to_cart(request, slug):
    try:
        produto = get_object_or_404(Produto, slug=slug)
        carrinho, created = Carrinho.objects.get_or_create(cliente=request.user)
        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho,
            produto=produto,
            defaults={'quantidade': 1},
        )
        if not created:
            item.quantidade += 1
            item.save()
        return redirect('cart')
    except Exception as e:
        print(e)
        messages.error(request, 'Erro ao adicionar o produto ao carrinho.')
        return redirect('product-detail', slug=slug)
    

class CategoriaListView(View):
    template_name = 'pages/product-list.html'

    def get(self, request, categoria_slug):
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.filter(categoria=categoria)
        context = {
            'categoria': categoria,
            'produtos': produtos
        }
        return render(request, self.template_name, context)
    

def health_check(request):
    return JsonResponse({"status": "healthy"})