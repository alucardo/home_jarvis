from django import forms

from time_manager.models import Category


class TimerForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        label="Kategoria",
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["category"].queryset = Category.objects.filter(user=self.user)
