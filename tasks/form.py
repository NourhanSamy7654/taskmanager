from django import forms
from datetime import date
from .models import Task

class taskform(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "status", "due_date"]
        widgets = {
    'title': forms.TextInput(attrs={'class': 'form-control'}),
    'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    'priority': forms.Select(attrs={'class': 'form-control'}),
    'status': forms.Select(attrs={'class': 'form-control'}),
    'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
}

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')

        if due_date and due_date < date.today():
            raise forms.ValidationError("Due date cannot be in the past.")

        return due_date