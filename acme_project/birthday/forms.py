from django import forms
# Импортируем класс ошибки валидации.
from django.core.exceptions import ValidationError

from .models import Birthday
from .validators import real_age


# Множество с именами участников Ливерпульской четвёрки.
BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=20)
    last_name = forms.CharField(
        label='Фамилия', required=False, help_text='Необязательное поле'
    )
    birthday = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
        # В аргументе validators указываем список или кортеж 
        # валидаторов этого поля (валидаторов может быть несколько).
        validators=(real_age,),
    )
    
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        fields = '__all__'  

        def clean_first_name(self):
            # Получаем значение имени из словаря очищенных данных.
            first_name = self.cleaned_data['first_name']
            # Разбиваем полученную строку по пробелам 
            # и возвращаем только первое имя.
            return first_name.split()[0]
        
        def clean(self):
            # Вызов родительского метода clean.
            super().clean()
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            if f'{first_name} {last_name}' in BEATLES:
                raise ValidationError(
                    'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
                )