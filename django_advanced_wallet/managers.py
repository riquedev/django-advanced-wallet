from django.db.models.fields.related import OneToOneField


def get_default_wallet():
    from .models import Wallet
    return Wallet.objects.create().pk


class WalletManager(OneToOneField):
    # Field flags
    many_to_many = False
    many_to_one = False
    one_to_many = False
    one_to_one = True

    def __init__(self, verbose_name=None, on_delete=None,
                 to_field=None, **kwargs):
        to = "django_advanced_wallet.Wallet"

        if 'to' in kwargs:
            del kwargs["to"]

        if "default" not in kwargs:
            kwargs["default"] = get_default_wallet

        super().__init__(to, verbose_name=verbose_name, on_delete=on_delete, to_field=to_field, **kwargs)
