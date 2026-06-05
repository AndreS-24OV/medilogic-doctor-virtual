from django.db import models

class Consulta(models.Model):
    sintomas = models.TextField()
    resultado = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta {self.id} - {self.fecha:%Y-%m-%d %H:%M}"
