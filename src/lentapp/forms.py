from django import forms


class BookSlotForm(forms.Form):

    date_start = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    time_start = forms.TimeField(
        label="Time",
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
    )
    duration = forms.FloatField(
        label="Duration",
        min_value=0,
        max_value=24,
        step_size=0.5,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
