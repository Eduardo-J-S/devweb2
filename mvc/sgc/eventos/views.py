from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento
from projeto.models import Projeto
from django.http import HttpResponse


def selecionar_projeto(request):
    projetos = Projeto.objects.all()
    if request.method == 'POST':
        projeto_id = request.POST.get('projeto_id')
        return redirect('criar_evento', projeto_id=projeto_id)
    return render(request, 'eventos/selecionar_projeto.html', {'projetos': projetos})

def listar_eventos(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    eventos = projeto.eventos.all()
    context = {'projeto': projeto, 'eventos': eventos}
    return render(request, 'eventos/list.html', context)

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
