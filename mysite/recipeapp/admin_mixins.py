import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str


class ExportAsCSVMixin:
    """
    Миксин для экспорта данных в CSV-файл.
    """

    def export_csv(self, request, queryset):
        """
        Экспортирует выбранные объекты в CSV-файл.
        """
        # Название модели
        model_name = self.model._meta.verbose_name_plural

        # Создаем HTTP-ответ с типом содержимого CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'

        # Создаем CSV-писатель
        writer = csv.writer(response, delimiter=';')

        # Заголовки столбцов
        headers = [smart_str(field.verbose_name) for field in self.model._meta.fields]
        writer.writerow(headers)

        # Данные
        for obj in queryset:
            row = [smart_str(getattr(obj, field.name)) for field in self.model._meta.fields]
            writer.writerow(row)

        return response

    export_csv.short_description = "Экспортировать выбранные объекты в CSV"
