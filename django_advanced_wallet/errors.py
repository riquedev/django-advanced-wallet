from django.db import IntegrityError

class NegativeAmount(IntegrityError):
    pass

class NonCanceableOperation(IntegrityError):
    pass

class InsufficentBalance(IntegrityError):
    """Raised when a wallet has insufficient balance to
       run an operation.
       We're subclassing from :mod:`django.db.IntegrityError`
       so that it is automatically rolled-back during django's
       transaction lifecycle.

       Based on https://github.com/thejpanganiban/django-pursed/blob/master/src/wallet/errors.py
       """
