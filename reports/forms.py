from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'title',
            'area',
            'tags',
            'image',
            'address',
            'lat',
            'lng',
            'description'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Report title'
            }),

            'area': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),

            'tags': forms.SelectMultiple(attrs={
                'class': 'select select-bordered w-full h-40'
            }),

            'address': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 2,
                'placeholder': 'Optional address'
            }),

            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),

            'image': forms.ClearableFileInput(attrs={
                'class': 'file-input file-input-bordered w-full'
            }),

            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 2,
                'placeholder': 'Optional address'
            }),
        }