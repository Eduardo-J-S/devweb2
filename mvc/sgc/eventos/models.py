from django.db import models
from projeto.models import Projeto

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data = models.DateTimeField()
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="eventos")

    def __str__(self):
        return f"{self.titulo} - {self.projeto.titulo}"
