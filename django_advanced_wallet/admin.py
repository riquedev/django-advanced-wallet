from django.contrib import admin
from .models import get_wallet_model, get_wallet_operation_model


@admin.register(get_wallet_model())
class WalletModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance', 'previous_balance')
    search_fields = ('id',)


@admin.register(get_wallet_operation_model())
class WalletOperationModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        """
        Skill disabled by default as it will not influence the wallet.
        Use the methods provided.
        """
        return False

    def has_add_permission(self, request):
        """
        Skill disabled by default as it will not influence the wallet.
        Use the methods provided.
        """
        return False
