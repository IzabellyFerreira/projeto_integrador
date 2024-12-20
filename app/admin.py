from django.contrib import admin
from django.http import HttpRequest
from .models import (
    Categoria, Marca, Produto, ImagemProduto, CustomUser, Venda, ItemVenda, Pagamento,
    EnderecoEntrega, Avaliacao, Comentario, Cupom, Carrinho, 
    ItemCarrinho, Desejo, ItemDesejo, Notificacao, Log
)

class BaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'criado_em'
    list_filter = ['criado_em', 'modificado_em']

    def get_list_display(self, request):
        return ['id'] + getattr(self, 'custom_list_display', []) + ['criado_em', 'modificado_em']


@admin.register(Categoria)
class CategoriaAdmin(BaseAdmin):
    custom_list_display = ['nome', 'slug']
    search_fields = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Marca)
class MarcaAdmin(BaseAdmin):
    custom_list_display = ['nome', 'slug']
    search_fields = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}


class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

@admin.register(Produto)
class ProdutoAdmin(BaseAdmin):
    custom_list_display = ['nome', 'slug', 'marca', 'categoria', 'preco']
    search_fields = ['nome', 'slug', 'marca__nome', 'categoria__nome']
    list_filter = BaseAdmin.list_filter + ['marca', 'categoria']
    prepopulated_fields = {'slug': ('nome',)}
    inlines = [ImagemProdutoInline]

admin.site.register(ImagemProduto)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'cpf', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined']
    search_fields = ['nome', 'email', 'cpf']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    readonly_fields = ['password']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email', 'cpf')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2') }),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email', 'cpf')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )


# class ItemVendaInline(admin.TabularInline):
#     model = ItemVenda
#     extra = 1


# @admin.register(Venda)
# class VendaAdmin(BaseAdmin):
#     custom_list_display = ['cliente']
#     search_fields = ['cliente__nome']
#     list_filter = BaseAdmin.list_filter + ['cliente']
#     inlines = [ItemVendaInline]


# @admin.register(Pagamento)
# class PagamentoAdmin(BaseAdmin):
#     custom_list_display = ['venda', 'valor']
#     search_fields = ['venda__id', 'valor']
#     list_filter = BaseAdmin.list_filter + ['venda']


# @admin.register(EnderecoEntrega)
# class EnderecoEntregaAdmin(BaseAdmin):
#     custom_list_display = ['venda', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep']
#     search_fields = ['venda__cliente__nome', 'rua', 'cidade', 'estado', 'cep']
#     list_filter = BaseAdmin.list_filter + ['venda__cliente']


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'cliente', 'estrelas', 'data']
    search_fields = ['cliente__username', 'produto__nome']
    list_filter = ['produto', 'cliente']


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['avaliacao', 'texto', 'data']
    search_fields = ['avaliacao__cliente__username', 'texto']
    list_filter = ['avaliacao__produto', 'avaliacao__cliente']


# @admin.register(Cupom)
# class CupomAdmin(BaseAdmin):
#     custom_list_display = ['codigo', 'desconto']
#     search_fields = ['codigo']
#     list_filter = BaseAdmin.list_filter


@admin.register(Carrinho)
class CarrinhoAdmin(BaseAdmin):
    custom_list_display = ['cliente']
    search_fields = ['cliente__nome']
    list_filter = BaseAdmin.list_filter + ['cliente']


@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(BaseAdmin):
    custom_list_display = ['carrinho', 'produto', 'quantidade']
    search_fields = ['carrinho__id', 'produto__nome', 'quantidade']
    list_filter = BaseAdmin.list_filter + ['carrinho', 'produto']


# @admin.register(Desejo)
# class DesejoAdmin(BaseAdmin):
#     custom_list_display = ['cliente']
#     search_fields = ['cliente__nome']
#     list_filter = BaseAdmin.list_filter + ['cliente']


# @admin.register(ItemDesejo)
# class ItemDesejoAdmin(BaseAdmin):
#     custom_list_display = ['desejo', 'produto']
#     search_fields = ['desejo__id', 'produto__nome']
#     list_filter = BaseAdmin.list_filter + ['desejo', 'produto']


# @admin.register(Notificacao)
# class NotificacaoAdmin(BaseAdmin):
#     custom_list_display = ['cliente', 'texto']
#     search_fields = ['cliente__nome', 'texto']
#     list_filter = BaseAdmin.list_filter + ['cliente']


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    custom_list_display = ['tabela', 'objeto', 'campo', 'valor_antigo', 'valor_novo', 'acao', 'usuario']
    search_fields = ['tabela', 'objeto', 'campo', 'acao', 'usuario__username']
    list_filter = ['tabela', 'acao', 'usuario', 'criado_em']
    readonly_fields = ['tabela', 'objeto', 'campo', 'valor_antigo', 'valor_novo', 'acao', 'usuario', 'criado_em']

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False