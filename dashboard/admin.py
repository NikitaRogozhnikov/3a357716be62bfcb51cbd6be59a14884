from django.contrib import admin
from .models import PlotInfo
from .task import convert, redis_instance
from datetime import datetime
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

        if request.method == 'POST': #если передали данные POST методом то обновляем отмеченные графики 
           for i in request.POST: #   
               if i !='csrfmiddlewaretoken':# выбираем из запроса только айдишники 
                   convert.apply_async((int(i),),countdown=1) #вызываем ассинхронную операцию обнвления данных

        else:          
            for one_plot in qs.values(): # иначе обновляем данные для всех функций                
                convert.apply_async((one_plot['id'],),countdown=1)           
        response.context_data['test']=qs.values() #формируем контекст
        return response
