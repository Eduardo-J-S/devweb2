from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento
from projeto.models import Projeto
from django.http import HttpResponse

def listar_eventos(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    eventos = projeto.eventos.all()
    context = {'projeto': projeto, 'eventos': eventos}
    return render(request, 'eventos/list.html', context)

def criar_evento(request):
    if request.method == 'POST':
        projeto_id = request.POST.get('projeto_id')
        projeto = get_object_or_404(Projeto, id=projeto_id)
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

    projetos = Projeto.objects.all()
    return render(request, 'eventos/form.html', {'projetos': projetos})

