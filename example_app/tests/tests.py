import os
from random import randrange
from django.test import TestCase
from django_advanced_wallet.models import Wallet
from django_advanced_wallet.errors import NegativeAmount, InsufficentBalance
from decimal import Decimal
if os.environ.get('DJANGO_EXAMPLE_APP') == "example_app.tests":
    from example_app.tests.models import Account, RelatedObject
else:
    from tests.models import Account, RelatedObject


class TestWalletRelation(TestCase):
    DEPOSIT_VALUES = list(sorted([randrange(100 * i, 200 * i) / 100 for i in range(1, 1000)]))

    def test_object_creation(self):
        obj = Account.objects.create()
        self.assertIsInstance(obj.wallet, Wallet)

    def test_deposit(self):
        obj = Account.objects.create()
        for value in self.DEPOSIT_VALUES:
            value = Wallet.normalize_amount(Decimal(value))
            self.assertEqual(obj.wallet.deposit(value).value, value)

    def test_deposit_with_related_object(self):
        obj = Account.objects.create()
        related_obj = RelatedObject.objects.create(name="test")

        for value in self.DEPOSIT_VALUES:
            value = Wallet.normalize_amount(Decimal(value))
            operation = obj.wallet.deposit(value, related_object=related_obj)
            self.assertEqual(operation.value, value)
            self.assertEqual(operation.content_object, related_obj)

    def test_negative_operation(self):
        obj = Account.objects.create()
        related_obj = RelatedObject.objects.create(name="test")
        with self.assertRaises(NegativeAmount):
            obj.wallet.withdraw(Decimal(-100))

    def test_insuffiecient_operation(self):
        obj = Account.objects.create()
        with self.assertRaises(InsufficentBalance):
            obj.wallet.withdraw(Decimal(100))

    def test_withdraw(self):
        obj = Account.objects.create()
        fund_200 = Wallet.normalize_amount(Decimal(200))
        fund_100 = Wallet.normalize_amount(Decimal(100))
        fund_0 = Wallet.normalize_amount(Decimal(0))
        obj.wallet.deposit(fund_200)

        self.assertEqual(obj.wallet.withdraw(fund_100).value, fund_100)
        self.assertEqual(obj.wallet.withdraw(fund_100).previous_value, fund_100)
        self.assertEqual(obj.wallet.balance, fund_0)

        with self.assertRaises(InsufficentBalance):
            obj.wallet.withdraw(fund_100)

    def test_withdraw_with_related_object(self):
        obj = Account.objects.create()
        related_obj = RelatedObject.objects.create(name="test")

        for value in self.DEPOSIT_VALUES:
            decimal_value = Wallet.normalize_amount(Decimal(value))
            obj.wallet.deposit(decimal_value)
            operation = obj.wallet.withdraw(decimal_value, related_object=related_obj)
            obj.refresh_from_db()

            self.assertEqual(operation.value, decimal_value)
            self.assertEqual(operation.content_object, related_obj)
            self.assertEqual(obj.wallet.previous_balance, operation.previous_value)

    def test_transfer(self):
        from_account = Account.objects.create()
        to_account = Account.objects.create()

        for value in self.DEPOSIT_VALUES:
            decimal_value = Wallet.normalize_amount(Decimal(value))
            zero_value = Wallet.normalize_amount(Decimal(0))
            from_account.wallet.deposit(decimal_value)
            from_account.refresh_from_db()

            self.assertEqual(from_account.wallet.balance, decimal_value)

            from_operation, to_operation = from_account.wallet.transfer(
                to_wallet=to_account.wallet,
                amount=decimal_value
            )

            self.assertEqual(from_operation.value, decimal_value)
            self.assertEqual(to_operation.value, decimal_value)
            self.assertEqual(from_operation.wallet.balance, zero_value)
            self.assertEqual(to_operation.wallet.balance, decimal_value)
            self.assertEqual(from_operation.operation_type, from_operation.OperationType.TRANSFER_ORIGIN)
            self.assertEqual(to_operation.operation_type, to_operation.OperationType.TRANSFER_DESTINATION)

            to_operation.wallet.withdraw(decimal_value)

    def test_operation_cancel(self):
        account = Account.objects.create()
        fund_0 = Wallet.normalize_amount(Decimal(0))
        fund_1000 = Wallet.normalize_amount(Decimal(1000))
        operation = account.wallet.deposit(
            fund_1000
        )
        self.assertEqual(account.wallet.balance, fund_1000)

        cancel_operation = operation.cancel_operation()
        account.refresh_from_db()

        self.assertEqual(cancel_operation.operation_type, cancel_operation.OperationType.WITHDRAW)
        self.assertEqual(account.wallet.balance, fund_0)

        for value in self.DEPOSIT_VALUES:
            decimal_value = Wallet.normalize_amount(Decimal(value))
            operation = account.wallet.deposit(decimal_value)
            self.assertEqual(account.wallet.balance, decimal_value)
            operation.cancel_operation()
            account.refresh_from_db()
            self.assertEqual(account.wallet.balance, fund_0)

    def test_force_withdraw(self):
        account = Account.objects.create()
        fund_0 = Wallet.normalize_amount(Decimal(0))
        fund_1000 = Wallet.normalize_amount(Decimal(1000))

        account.wallet.deposit(
            fund_1000
        )

        self.assertEqual(account.wallet.balance, fund_1000)
        account.wallet.withdraw(fund_1000)
        self.assertEqual(account.wallet.balance, fund_0)

        with self.assertRaises(InsufficentBalance):
            account.wallet.withdraw(fund_1000)

        account.wallet.withdraw(fund_1000, force_withdraw=True)
        self.assertEqual(account.wallet.balance, fund_1000 * -1)
