from django import forms


class EquipoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre del equipo",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "w-full bg-slate-900/80 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors",
            "placeholder": "Ej. Cámara Canon EOS R5",
        }),
    )
    categoria = forms.CharField(
        label="Categoría",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "w-full bg-slate-900/80 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors",
            "placeholder": "Ej. Fotografía",
        }),
    )
    precio_dia = forms.DecimalField(
        label="Precio de alquiler por día (S/)",
        min_value=0,
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "w-full bg-slate-900/80 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors",
            "placeholder": "Ej. 50.00",
            "step": "0.01",
        }),
    )
    stock = forms.IntegerField(
        label="Cantidad en stock",
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "w-full bg-slate-900/80 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors",
            "placeholder": "Ej. 2",
        }),
    )