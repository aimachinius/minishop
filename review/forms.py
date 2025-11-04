from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']
        labels = {
            'rating': 'Đánh giá ',
            'comment': 'Bình luận',
        }
        widgets = {
            'rating':forms.Select(attrs={'class':'form-select'}),
            'comment': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
        }