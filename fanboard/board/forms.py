from django.contrib.auth.models import User
from .models import Ad
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Response


class AdCreationForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'text', 'image', 'video']
        widgets = {
            'text': CKEditorWidget(),
        }


class AdUpdateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'image', 'video']
        widgets = {
            'text': CKEditorWidget(),
        }


class AdDeletionForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].widget.attrs['value'] = 'delete'
        self.fields['action'].widget.attrs['style'] = 'display: none'

    action = forms.CharField(widget=forms.HiddenInput())


class AdUpdateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'text', 'image', 'video']
        widgets = {
            'text': CKEditorWidget(),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        labels = {'text': 'Текст отклика'}


class DateFilterForm(forms.Form):
    date = forms.DateField(label='Дата', required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class CategoryFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]
    category = forms.ChoiceField(label='Категория', choices=CATEGORY_CHOICES, required=False)


class UserFilterForm(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.all(), label='Пользователь', required=False)
