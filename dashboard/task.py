from TestTask.celery import app
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols
import numpy as np
from datetime import datetime, date, timedelta
from datetime import time as tt
import time
import matplotlib as mp
mp.use('Agg')
import pylab as plt
import  io
import  urllib, base64
from .models import PlotInfo
import redis
from TestTask import settings
from celery import shared_task
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=settings.REDIS_DB)    
@app.task
#@shared_task
def convert(id): # функция формирования графика
    norm_koef=10e18 # нормировачный коэффициент т.к для вычислений использует unixtime
    plot_info_object=PlotInfo.objects.get(pk=id)# получаем запись в БД по айдишнику
    fun=plot_info_object.fun # строковое значение функции
    interval=plot_info_object.interval # интервал
    step=plot_info_object.step # шаг в часах
    plot_info_object.actualdate=datetime.now()# обновляем актуалное время
    redis_instance.set(str(id),str(datetime.now())) #записываем время в redis   
    try:
        err=False
        equation=parse_expr(fun,evaluate=False)# парсим выражение
        timestep=step*60*60 
        dtnow=time.mktime(datetime.now().timetuple())# текущее unixtime время 
        t=datetime.now()-timedelta(days=interval)# интервал времени
        dt=time.mktime(t.timetuple())# переводим интервал в юникстайм
        calk=lambda p: float(equation.subs(symbols('t'), p))# метод для вычисления функции
        x=np.arange(dt,dtnow,timestep)# формируем массив данных
        x_date=list(map(datetime.fromtimestamp,x))# переводим обратно в понятное время
        y=list(map(calk,x))# вычисляем функцию
        y_norm=[i/norm_koef for i in y]# нормируем данные
        plt.plot(x_date,y_norm) # строим и сохраняем график
        fig=plt.gcf()
        plt.close()
        buf=io.BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        string=base64.b64encode(buf.read())
        uri=urllib.parse.quote(string)
        err=False
    except Exception as exception:
        uri=exception.__class__.__name__
        err=True
    finally:
       
        #redis_instance.set(fun,uri) 
        plot_info_object.graph=uri#redis_instance.get(fun)# передаем гафик в БД
        plot_info_object.save()# сохраняем БД
          
    return {'graph':uri,'fun':fun,'step':step,'interval':interval,'actualdate':datetime.now(), 'id':id,'error':err}
    