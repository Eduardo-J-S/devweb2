# Atividade: Criando um Novo Aplicativo "Eventos"

Vamos criar um aplicativo chamado "eventos", onde será possível gerenciar eventos relacionados aos projetos existentes. Assim, cada projeto poderá ter eventos associados, como reuniões, apresentações ou prazos importantes.

# Por que criar um novo aplicativo?
Em projetos Django, é comum dividir funcionalidades em aplicativos separados para manter o código organizado. O aplicativo "eventos" será responsável por gerenciar eventos, enquanto o aplicativo "projeto" cuida dos projetos institucionais. Isso permite que cada parte do sistema tenha suas próprias views, modelos e templates, facilitando o desenvolvimento e a manutenção.

## 1. Criar um Novo Aplicativo
Execute o comando para criar o novo aplicativo:
`python manage.py startapp eventos`

Adicione o aplicativo `eventos` em `INSTALLED_APPS` no arquivo `settings.py`:

```python
INSTALLED_APPS = [
    # outros apps
    'eventos',
]
```

## 2. Modelo de Evento
Crie o modelo para representar os eventos. Cada evento estará relacionado a um projeto.

Em: `eventos/models.py`

```python
from projeto.models import Projeto

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data = models.DateTimeField()
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="eventos")

    def __str__(self):
        return f"{self.titulo} - {self.projeto.titulo}"
```
Os modelos representam as tabelas do banco de dados. Cada classe no `models.py` será traduzida em uma tabela, com cada atributo da classe se tornando uma coluna.
O modelo `Evento` tem atributos como `titulo`, `descricao` e `data`, que serão armazenados no banco de dados. O atributo `projeto` cria uma relação entre eventos e projetos, permitindo associar múltiplos eventos a um único projeto.

### Rode as migrações para atualizar o banco de dados:
```
python manage.py makemigrations eventos
python manage.py migrate
```

## 3. Views para Gerenciamento de Eventos
Em: `eventos/views.py`

**Listar Eventos:**
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento
from projeto.models import Projeto

def listar_eventos(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    eventos = projeto.eventos.all()
    context = {'projeto': projeto, 'eventos': eventos}
    return render(request, 'eventos/list.html', context)
```

**Criar Evento:**
```python
from django.http import HttpResponse

def criar_evento(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        if titulo and data:
            Evento.objects.create(
                titulo=titulo,
                descricao=descricao,
                data=data,
                projeto=projeto
            )
            return redirect('listar_eventos', projeto_id=projeto.id)
    return render(request, 'eventos/form.html', {'projeto': projeto})
```
**Selecionar Projeto**
```python
def selecionar_projeto(request):
    projetos = Projeto.objects.all()
    if request.method == 'POST':
        projeto_id = request.POST.get('projeto_id')
        return redirect('criar_evento', projeto_id=projeto_id)
    return render(request, 'eventos/selecionar_projeto.html', {'projetos': projetos})
```

As views no Django são responsáveis por processar as requisições do usuário e retornar respostas. Elas são a ponte entre o modelo (dados) e os templates (interface).
- A view `listar_eventos` busca os eventos do banco de dados e os envia para o template `list.html`, que exibe os dados.
- A view `criar_evento` lida com o formulário de criação de eventos, salva os dados no banco e redireciona o usuário após o sucesso.
- A view `selecionar_projeto` implementa a lógica para exibir e processar o formulário de seleção de projeto.

## 4. Templates

**Listar Eventos**
Arquivo: `templates/eventos/list.html`

```html
{% extends 'base.html' %}
{% block title %}Eventos de {{ projeto.titulo }}{% endblock %}
{% block content %}
<h1>Eventos de "{{ projeto.titulo }}"</h1>
<ul>
    {% for evento in eventos %}
        <li>
            <strong>{{ evento.titulo }}</strong>: {{ evento.data|date:"d/m/Y H:i" }}
            <p>{{ evento.descricao }}</p>
        </li>
    {% endfor %}
</ul>
<a href="{% url 'criar_evento' projeto.id %}" class="btn btn-primary">Adicionar Evento</a>
<a href="{% url 'listar' %}">Voltar para Projetos</a>
{% endblock %}
```

**Criar Evento**
Arquivo: `templates/eventos/form.html`

```html
{% extends 'base.html' %}
{% block title %}Criar Evento para {{ projeto.titulo }}{% endblock %}
{% block content %}
<h1>Criar Evento para "{{ projeto.titulo }}"</h1>
<form method="post">
    {% csrf_token %}
    <label for="titulo">Título:</label>
    <input type="text" name="titulo" id="titulo" required>
    <label for="descricao">Descrição:</label>
    <textarea name="descricao" id="descricao"></textarea>
    <label for="data">Data:</label>
    <input type="datetime-local" name="data" id="data" required>
    <button type="submit" class="btn btn-primary">Salvar</button>
</form>
<a href="{% url 'listar_eventos' projeto.id %}">Cancelar</a>
{% endblock %}
```

**Template para Seleção de Projeto**
Arquivo: `templates/eventos/selecionar_projeto.html`
```html
{% extends 'base.html' %}
{% block title %}Selecionar Projeto{% endblock %}
{% block content %}
<h1>Selecionar Projeto</h1>
<form method="post">
    {% csrf_token %}
    <label for="projeto_id">Projeto:</label>
    <select name="projeto_id" id="projeto_id" required>
        {% for projeto in projetos %}
            <option value="{{ projeto.id }}">{{ projeto.titulo }}</option>
        {% endfor %}
    </select>
    <button type="submit">Continuar</button>
</form>
{% endblock %}

```

Os templates são arquivos HTML que recebem dados das views para criar a interface do usuário. No Django, podemos usar tags do template engine, como `{% for evento in eventos %}` para iterar sobre os dados recebidos e exibi-los dinamicamente.
No template `list.html`, usamos `{% extends 'base.html' %}` para herdar o layout geral da aplicação, como o cabeçalho e o rodapé. Os blocos `{% block title %}` e `{% block content %}` permitem que cada página substitua partes específicas do layout base.

## 5. URLs do Aplicativo "Eventos"
No arquivo `eventos/urls.py`, configure as rotas específicas para o gerenciamento de eventos:

```python
from django.urls import path

from . import views 

urlpatterns = [
    path('selecionar/', views.selecionar_projeto, name='selecionar_projeto'),
    path('<int:projeto_id>/eventos/', views.listar_eventos, name='listar_eventos'),
    path('<int:projeto_id>/eventos/novo/', views.criar_evento, name='criar_evento'),
]
```
`selecionar/`: Permite que o usuário selecione um projeto a partir de uma lista, antes de realizar ações como criar ou listar eventos.
`<int:projeto_id>/eventos/`: Exibe uma lista com todos os eventos associados a um projeto específico. 
`<int:projeto_id>/eventos/novo/`: Permite que o usuário crie um novo evento para um projeto específico.

## 6. Configuração de URLs
No arquivo de configuração principal `sgc/urls.py`, atualize as rotas para incluir o novo aplicativo "eventos". Isso permitirá que as funcionalidades do novo aplicativo sejam acessíveis a partir das URLs..
Arquivo `sgc/urls.py` atualizado: 

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('projeto/', include('projeto.urls')),  
    path('eventos/', include('eventos.urls')), 
]
```

O Django Admin é uma ferramenta para gerenciar dados de forma visual. Ao registrar o modelo `Evento`, podemos criar, editar e excluir eventos diretamente no painel administrativo, o que é útil durante o desenvolvimento.

## 7. Atualizar o Admin
Adicione a funcionalidade de gerenciamento de eventos no Django Admin.

Arquivo: `eventos/admin.py`

```python
from django.contrib import admin
from .models import Evento

admin.site.register(Evento)
```

## 8. Iniciar o servidor:
- Garanta que todas as dependências estão instaladas: Certifique-se de que o ambiente virtual está ativado e os pacotes necessários estão instalados:
`pip install -r requirements.txt`

- Inicie o servidor de desenvolvimento: Execute o comando abaixo para iniciar o servidor local:
`python manage.py runserver` 

Acesse a aplicação no navegador: O servidor será iniciado no endereço http://127.0.0.1:8000/. A partir daí, você pode navegar pelas rotas configuradas.

Listar Projetos: `http://127.0.0.1:8000/projeto/`

Listar Eventos de um Projeto: `http://127.0.0.1:8000/eventos/<projeto_id>/eventos/`

Selecionar projeto para adicionar evento: `http://127.0.0.1:8000/eventos/selecionar/`

# Tarefas em Aberto

As tarefas em aberto são desafios extras para praticar o que foi aprendido.
**Editar e excluir eventos:** Criar views e templates para editar e excluir eventos associados aos projetos.

