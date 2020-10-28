from django.db import models
from datetime import datetime
class PlotInfo(models.Model):
    """
    docstring
    """
    fun=models.CharField(max_length=50,help_text="Введите вашу функцию от t")
    interval=models.IntegerField(help_text='Интервал времени в днях')
    step=models.IntegerField(help_text='Шаг моделирования в часах')
    graph=models.TextField(editable=False)
    actualdate=models.DateTimeField(default=datetime.now(),editable=False)
    def __str__(self):
        return self.fun
