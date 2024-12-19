from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


###################################################################
# MODELAGEM DE BANCO DE DADOS PARA UMA LOJA DE PRODUTOS DE BELEZA #
###################################################################


# Categoria de produtos (ex: cabelo, pele, maquiagem)
class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


# Marca de produtos (ex: Natura, Avon, O Boticário)
class Marca(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nome



# Produto (ex: shampoo, condicionador, batom, base)
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fabricacao = models.DateField()
    validade = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    imagem_principal = models.ImageField(upload_to='produtos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/')

    def __str__(self):
        return f'Imagem de {self.produto.nome}'


# Usuário customizado (ex: Maria, João, Ana)
# Herda da classe AbstractUser do Django
class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name='CPF')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.username


########################################################################
# Venda (ex: venda de 3 shampoos, 2 condicionadores e 1 batom para Maria)
class Venda(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        return f'Venda {self.id} - Cliente {self.cliente.nome}'   
    

########################################################################
# Itens da venda (ex: 3 shampoos, 2 condicionadores e 1 batom)
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens das Vendas'

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'
    

########################################################################
# Pagamento (ex: pagamento de R$ 100,00 em dinheiro)
class Pagamento(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return f'Pagamento {self.id} - R$ {self.valor}'
    

########################################################################
# Endereço de entrega (ex: entrega na Rua A, número 123, bairro B)
class EnderecoEntrega(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Endereço de Entrega'
        verbose_name_plural = 'Endereços de Entrega'

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'
    

# Avaliação do produto (ex: avaliação de 5 estrelas para o shampoo)
class Avaliacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    estrelas = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f'{self.estrelas} estrelas - {self.cliente.username} sobre {self.produto.nome}'


# Comentário sobre a avaliação (ex: comentário sobre a avaliação do shampoo)
class Comentario(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return f'Comentário de {self.avaliacao.cliente.username}: {self.texto[:30]}...'
    

########################################################################
# Cupom de desconto (ex: cupom de 10% de desconto)
class Cupom(models.Model):
    codigo = models.CharField(max_length=255)
    desconto = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cupom'
        verbose_name_plural = 'Cupons'

    def __str__(self):
        return f'Cupom {self.codigo} - Desconto: R$ {self.desconto}'
    

# Carrinho de compras (ex: carrinho com 3 shampoos, 2 condicionadores e 1 batom)
class Carrinho(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    def __str__(self):
        return f'Carrinho {self.id} - Cliente: {self.cliente.username}'
    

# Itens do carrinho (ex: 3 shampoos, 2 condicionadores e 1 batom)
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} no carrinho de {self.carrinho.cliente.username}'
    

########################################################################
# Desejo de compra (ex: desejo de comprar 3 shampoos, 2 condicionadores e 1 batom)
class Desejo(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Desejo'
        verbose_name_plural = 'Desejos'

    def __str__(self):
        return f'Desejo {self.id} - Cliente: {self.cliente.nome}'


########################################################################
# Itens do desejo (ex: 3 shampoos, 2 condicionadores e 1 batom)
class ItemDesejo(models.Model):
    desejo = models.ForeignKey(Desejo, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item do Desejo'
        verbose_name_plural = 'Itens dos Desejos'

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} no desejo de {self.desejo.cliente.nome}'
    

########################################################################
# Notificação (ex: notificação de promoção de shampoo)
class Notificacao(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return f'Notificação para {self.cliente.nome}: {self.texto[:30]}...'
    

# Classe para registro de logs de alterações no banco de dados,
# mantém salvo a tabela, o objeto, o campo alterado, o valor antigo,
# o valor novo, a data de alteração, a ação realizada e o usuário.
class Log(models.Model):
    tabela = models.CharField(max_length=255)
    objeto = models.IntegerField()
    campo = models.CharField(max_length=255)
    valor_antigo = models.TextField()
    valor_novo = models.TextField()
    acao = models.CharField(max_length=255)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True) # Arrumar depois
    data = models.DateTimeField(auto_now_add=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def __str__(self):
        return f'[{self.data}] {self.acao} em {self.tabela} por {self.usuario}'