from django.conf import settings

WALLET_ID_LENGTH = getattr(settings,'WALLET_ID_LENGTH', 12)
OPERATION_ID_LENGTH = getattr(settings, 'WALLET_OPERATION_ID_LENGTH',15)
WALLET_DECIMAL_PLACES = getattr(settings, 'WALLET_DECIMAL_PLACES', 2)
WALLET_MAX_DIGITS = getattr(settings, 'WALLET_MAX_DIGITS', 10)
ALLOW_NEGATIVE_BALANCE = getattr(settings, 'WALLET_ALLOW_NEGATIVE_BALANCE', False)
WALLET_OPERATION_MODEL = getattr(settings, 'WALLET_OPERATION_MODEL', "django_advanced_wallet.WalletOperation")
WALLET_MODEL = getattr(settings, 'WALLET_MODEL', "django_advanced_wallet.Wallet")