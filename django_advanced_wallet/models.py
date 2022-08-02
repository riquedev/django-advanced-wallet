try:
    from __future__ import annotations
except SyntaxError:
    pass
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.apps import apps
from .app_settings import (WALLET_ID_LENGTH, WALLET_DECIMAL_PLACES, OPERATION_ID_LENGTH, WALLET_MAX_DIGITS,
                           ALLOW_NEGATIVE_BALANCE, WALLET_MODEL, WALLET_OPERATION_MODEL)
from .errors import (InsufficentBalance, NegativeAmount, NonCanceableOperation)
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

def get_operation_id():
    return get_random_string(OPERATION_ID_LENGTH)


def get_wallet_id():
    return get_random_string(WALLET_ID_LENGTH)

def get_wallet_operation_model():
    return apps.get_model(WALLET_OPERATION_MODEL)

def get_wallet_model():
    return apps.get_model(WALLET_MODEL)


class WalletManager(models.Manager):

    def deposit(self, wallet: int | 'Wallet', amount: Decimal, name: str = _("Deposit"),
                description: str = _("Simple deposit"),
                related_operation: 'WalletOperation' = None, related_object: models.Model = None) -> 'WalletOperation':
        with transaction.atomic():
            pk = wallet

            if isinstance(wallet, get_wallet_model()):
                pk = wallet.pk

            wallet = get_wallet_model().objects.select_for_update().get(pk=pk)
            wallet.previous_balance = wallet.balance
            amount = get_wallet_model().normalize_amount(amount)

            ct_type = None
            if related_object:
                ct_type = ContentType.objects.get(
                    app_label=related_object._meta.app_label,
                    model=related_object._meta.model_name
                )

            assert isinstance(amount, Decimal), _(
                "Please, to ensure maximum precision use the \"Decimal\" class (from decimal import Decimal)")

            if amount < Decimal(0):
                raise NegativeAmount(_("%(amount)s is an invalid value for this operation"))

            operation = get_wallet_operation_model().objects.create(
                name=name,
                description=description,
                related_operation=related_operation,
                value=amount,
                wallet=wallet,
                previous_value=wallet.previous_balance,
                content_type=ct_type,
                object_id=getattr(related_object, "pk", None),
                operation_type=get_wallet_operation_model().OperationType.DEPOSIT
            )
            wallet.balance += amount
            wallet.save()
            return operation

    def withdraw(self, wallet: int | 'Wallet', amount: Decimal, name: str = _("Withdraw"),
                 description: str = _("Simple withdraw"),
                 related_operation: WalletOperation = None, related_object: models.Model = None,
                 force_withdraw: bool = False) -> WalletOperation:
        with transaction.atomic():
            pk = wallet

            if isinstance(wallet, get_wallet_model()):
                pk = wallet.pk

            wallet = get_wallet_model().objects.select_for_update().get(pk=pk)
            wallet.previous_balance = wallet.balance
            amount = get_wallet_model().normalize_amount(amount)

            ct_type = None
            if related_object:
                ct_type = ContentType.objects.get(
                    app_label=related_object._meta.app_label,
                    model=related_object._meta.model_name
                )

            assert isinstance(amount, Decimal), _(
                "Please, to ensure maximum precision use the \"Decimal\" class (from decimal import Decimal)")
            is_negative_operation = wallet.balance - amount < 0

            if is_negative_operation and not ALLOW_NEGATIVE_BALANCE and not force_withdraw:
                raise InsufficentBalance(
                    _("There are not enough funds in the wallet to perform this operation.\nRequest: %(amount)s\nBalance: %(balance)s") % {
                        "amount": amount,
                        "balance": wallet.balance
                    })

            if amount < Decimal(0):
                raise NegativeAmount(_("%(amount)s is an invalid value for this operation"))

            operation = get_wallet_operation_model().objects.create(
                name=name,
                description=description,
                related_operation=related_operation,
                value=amount,
                wallet=wallet,
                previous_value=wallet.balance,
                content_type=ct_type,
                object_id=getattr(related_object, "pk", None),
                operation_type=get_wallet_operation_model().OperationType.WITHDRAW
            )

            wallet.balance -= amount
            wallet.save()
            return operation

    def transfer(self, from_wallet: int | 'Wallet', to_wallet: int | 'Wallet', amount: Decimal,
                 name: str = _("Transfer"), description: str = _("Simple transfer"),
                 related_object: models.Model = None) -> tuple[WalletOperation, WalletOperation]:
        pk_from = from_wallet
        pk_to = to_wallet

        if isinstance(from_wallet, get_wallet_model()):
            pk_from = from_wallet.pk
        if isinstance(to_wallet, get_wallet_model()):
            pk_to = to_wallet.pk

        withdraw_object = self.withdraw(pk_from, amount, name, description, related_object=related_object)
        deposit_object = self.deposit(pk_to, amount, name, description, related_operation=withdraw_object,
                                      related_object=related_object)
        withdraw_object.related_operation = deposit_object

        withdraw_object.operation_type = withdraw_object.OperationType.TRANSFER_ORIGIN
        deposit_object.operation_type = deposit_object.OperationType.TRANSFER_DESTINATION

        withdraw_object.save()
        deposit_object.save()
        return withdraw_object, deposit_object


class AbstractWalletOperation(TimeStampedModel, models.Model):
    class OperationType(models.TextChoices):
        DEPOSIT = 'DT', _('Deposit')
        WITHDRAW = 'WD', _('Withdraw')
        TRANSFER_ORIGIN = 'TO', _('Transfer Origin')
        TRANSFER_DESTINATION = 'TD', _('Transfer Destination')

    id = models.CharField(_("Operation id"), max_length=OPERATION_ID_LENGTH, primary_key=True,
                          default=get_operation_id)
    wallet = models.ForeignKey(WALLET_MODEL, db_index=True, on_delete=models.CASCADE, verbose_name=_("Wallet"),
                               related_name='wallet_operations', related_query_name='wallet_operations')
    related_operation = models.ForeignKey(WALLET_OPERATION_MODEL, db_index=True, blank=True, null=True,
                                          verbose_name=_("Related operation"), on_delete=models.SET_NULL,
                                          related_name='wallet_related_operations',
                                          related_query_name='wallet_related_operations')
    post_cancel_operation = models.ForeignKey(WALLET_OPERATION_MODEL, db_index=True, blank=True, null=True,
                                              verbose_name=_("Post cancellation operation"), on_delete=models.SET_NULL,
                                              related_name='wallet_post_cancel_operation',
                                              related_query_name='wallet_post_cancel_operation')
    name = models.CharField(_("Operation name"), max_length=360, default=_("Wallet Operation"))
    description = models.TextField(_("Operation description"), blank=True)
    value = models.DecimalField(_("Operation value"), decimal_places=WALLET_DECIMAL_PLACES, default=Decimal(0),
                                max_digits=WALLET_MAX_DIGITS)
    previous_value = models.DecimalField(_("Previous wallet value"), decimal_places=WALLET_DECIMAL_PLACES,
                                         default=Decimal(0), max_digits=WALLET_MAX_DIGITS)
    cancel = models.BooleanField(_("Operation cancel"), default=False, db_index=True)
    cancel_cause = models.TextField(_("Operation cancel cause"), blank=True)
    operation_type = models.CharField(max_length=2, choices=OperationType.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    object_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def cancel_operation(self):

        if self.operation_type in [self.OperationType.TRANSFER_ORIGIN, self.OperationType.TRANSFER_DESTINATION]:
            raise NonCanceableOperation(
                _("Transfer operations cannot be cancelled, it will be necessary to carry out the transfer in the wallet")
            )
        new_operation = None
        if self.operation_type == self.OperationType.DEPOSIT:
            new_operation = self.wallet.withdraw(
                amount=self.value,
                name=_("Operation Cancellation"),
                description=_("Abatement of value after cancellation of the operation \"%(name)s\"") % {
                    "name": self.name},
                related_operation=self,
                force_withdraw=True
            )
        elif self.operation_type == self.OperationType.WITHDRAW:
            new_operation = self.wallet.deposit(
                amount=self.value,
                name=_("Operation Cancellation"),
                description=_("Abatement of value after cancellation of the operation \"%(name)s\"") % {
                    "name": self.name},
                related_operation=self
            )

        return new_operation

    class Meta:
        verbose_name = _("Operation")
        verbose_name_plural = _("Operations")
        abstract = True


class AbstractWallet(TimeStampedModel, models.Model):
    id = models.CharField(_("Wallet id"), max_length=WALLET_ID_LENGTH, primary_key=True,
                          default=get_wallet_id)
    balance = models.DecimalField(_("Balance"), decimal_places=WALLET_DECIMAL_PLACES, default=Decimal(0),
                                  db_index=True,
                                  max_digits=WALLET_MAX_DIGITS)
    previous_balance = models.DecimalField(_("Previous balance"), decimal_places=WALLET_DECIMAL_PLACES,
                                           default=Decimal(0), db_index=True, max_digits=WALLET_MAX_DIGITS)

    objects = WalletManager()

    def deposit(self, amount: Decimal, name: str = _("Deposit"), description: str = _("Simple deposit"),
                related_operation: WalletOperation = None, related_object: models.Model = None) -> WalletOperation:
        result = get_wallet_model().objects.deposit(
            self,
            amount,
            name,
            description,
            related_operation,
            related_object
        )
        self.refresh_from_db()
        return result

    @staticmethod
    def normalize_amount(amount: Decimal):
        return round(amount, WALLET_DECIMAL_PLACES)

    def withdraw(self, amount: Decimal, name: str = _("Withdraw"), description: str = _("Simple withdraw"),
                 related_operation: WalletOperation = None, related_object: models.Model = None,
                 force_withdraw: bool = False):
        result = get_wallet_model().objects.withdraw(
            self,
            amount,
            name,
            description,
            related_operation,
            related_object,
            force_withdraw
        )
        self.refresh_from_db()
        return result

    def transfer(self, to_wallet: int | 'Wallet', amount: Decimal,
                 name: str = _("Transfer"), description: str = _("Simple transfer"),
                 related_object: models.Model = None) -> tuple[WalletOperation, WalletOperation]:
        result = get_wallet_model().objects.transfer(
            from_wallet=self,
            to_wallet=to_wallet,
            amount=amount,
            name=name,
            description=description,
            related_object=related_object
        )
        self.refresh_from_db()
        return result

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallet's")
        abstract = True


class WalletOperation(AbstractWalletOperation):
    pass


class Wallet(AbstractWallet):
    pass
