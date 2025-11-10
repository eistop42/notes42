from django import forms

from .models import NoteCategory, Note


class AddNoteForm(forms.Form):
    title = forms.CharField(label='заголовок')
    text = forms.CharField(widget=forms.Textarea, label='текст')
    category = forms.ModelChoiceField(
        queryset=NoteCategory.objects.all(),
        label='категория',
        empty_label='без категории',
        required=False
    )
    image = forms.FileField(label='картинка', required=False)

    def clean_title(self):
        title = self.cleaned_data['title']
        # проверить, есть ли такие заголовки в базе

        if Note.objects.filter(title=title).exists():
            raise forms.ValidationError('такой заголовок уже есть')

        return title


class AddNoteModelForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'без категории'