# events/forms.py

from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    # Formun görünümünü ve davranışını iyileştirmek için ek ayarlar
    # Tarih alanı için HTML5 date widget'ı kullanalım, böylece takvim çıkar
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # Saat alanı için HTML5 time widget'ı kullanalım
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Event  # Bu formun hangi modelden türetileceğini belirtiyoruz

        # Formda gösterilecek alanları belirliyoruz.
        # Otomatik olarak doldurulan alanları (organizer, created_at vs.) hariç tutuyoruz.
        fields = [
            'title', 'description', 'location', 'image', 'date', 'time',
            'capacity', 'tags', 'category'
        ]

        # Form elemanlarına daha güzel görünmeleri için Bootstrap CSS sınıfları ekleyebiliriz.
        # Bu, bir sonraki adımda HTML template'i oluştururken işimizi kolaylaştıracak.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'örn: müzik, ücretsiz'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }