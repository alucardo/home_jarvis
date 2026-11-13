from django import forms

from time_manager.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
        }
        labels = {'name': 'Nazwa'}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError("Taka kategoria już istnieje.")
        return name