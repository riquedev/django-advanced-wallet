from django import forms
from .models import get_wallet_model, get_wallet_operation_model


class WalletOperationForm(forms.ModelForm):
    class Meta:
        model = get_wallet_operation_model()
        fields = ('name', 'description', 'value', 'operation_type')
