from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Введите дату между текущей датой и 4 неделями (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < datetime.date.today():
            raise ValidationError(_('Новая дата возврата не может быть в прошлом!'))

        # Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Новая дата не может быть больше текущей более, чем на 4 недели!'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data