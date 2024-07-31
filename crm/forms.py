from django import forms
from django.forms import inlineformset_factory
from .models import Client, ClientProfil, Telephone, Abonnement, Version
from datetime import datetime, timedelta


class AbonnementForm(forms.ModelForm):
    class Meta:
        model = Abonnement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # # Ensure `type_abonnement` is initialized
        # type_abonnement_id = None
        
        # if 'type_abonnement' in self.data:
        #     try:
        #         type_abonnement_id = int(self.data.get('type_abonnement'))
        #         self.fields['version_offre'].queryset = Version.objects.filter(abonnement_type_id=type_abonnement_id).order_by('version')
        #     except (ValueError, TypeError):
        #         self.fields['version_offre'].queryset = Version.objects.none()
        # elif self.instance.pk:
        #     type_abonnement_id = self.instance.type_abonnement.id
        #     self.fields['version_offre'].queryset = Version.objects.filter(abonnement_type_id=type_abonnement_id).order_by('version')



class FilterForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

class DateFilterForm(forms.Form):
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = first_day_of_month.replace(day=1, month=first_day_of_month.month % 12 + 1) - timedelta(days=1)

    from_date = forms.DateField(
        label='From Date',
        initial=first_day_of_month,
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    to_date = forms.DateField(
        label='To Date',
        initial=last_day_of_month,
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

