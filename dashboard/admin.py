from django.contrib import admin
from .models import PlotInfo
from .task import convert, redis_instance
from datetime import datetime
from functools import reduce
@admin.register(PlotInfo)
class PlotInfoAdmin(admin.ModelAdmin):
    change_list_template = 'admin/dashboard.html'# базовый шаблон для изменения админ панели
    def changelist_view(self, request, extra_context=None): # метод для редактирования экземпляра модели
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
       
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response   
        tasks=[]

        def AND(a,b):
            return a and b

        def check_queue(queue): #проверка очереди
            while True:
                if 'FAILURE' in ' '.join([i.status for i in queue]): continue
                else: break
            while True:
                if reduce(AND,[i.ready() for i in queue]):break
    
        #формируем контекст
        for one_plot in qs.values(): # иначе обновляем данные для всех функций                         
            r=convert.apply_async((one_plot['id'],))
            tasks.append(r)        

        check_queue(tasks)
        response.context_data['test']=[j.get() for j in tasks]#qs.values()#
        return response
