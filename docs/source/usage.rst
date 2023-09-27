Usage
-----

To use `django_advanced_wallet` in your Django project, follow these steps:

1. **Add to INSTALLED_APPS**: Open your project's Django settings file (usually `settings.py`) and add `'django_advanced_wallet'` to the `INSTALLED_APPS` list:

   .. code-block:: python

      INSTALLED_APPS = (
          # ...
          'django_advanced_wallet',
          # ...
      )

   This step enables the `django_advanced_wallet` application in your project.

2. **Database Migrations**: Run Django's database migration commands to create the necessary database tables:

   .. code-block:: shell

      python manage.py migrate

   This will set up the database tables required for the wallet functionality.

3.**Now you will need to added a wallet manager**: for the model you intend to use, see the example below:
    .. code-block:: python

         from django.db import models
         from django_advanced_wallet.managers import WalletManager
         from django_advanced_wallet.models import Wallet

         class Account(models.Model):
            wallet: Wallet = WalletManager(on_delete=models.CASCADE)

4. **Using the Wallet**: Now you can start using `django_advanced_wallet` features in your Django project. Below are some common tasks you can perform with the wallet:

   a. **Creating a Wallet**: You can create a wallet for a user or an entity by using the `Wallet` model provided by `django_advanced_wallet`. Example:

    .. code-block:: python

         from django.db import models
         from myapp.models import Account

         obj = Account.objects.create()

   b. **Adding Funds**: To add funds to a wallet, use the `deposit` method. Example:

      .. code-block:: python

         from decimal import Decimal
         obj.wallet.deposit(Decimal("100.00"))

   c. **Making Transactions**: Perform transactions between wallets using the `Transaction` model. Example:

      .. code-block:: python

         from django_advanced_wallet.models import Transaction

         # Transfer funds from one wallet to another
         obj.wallet.transfer(to_wallet, amount=Decimal("100.00"))

   d. **Checking Wallet Balance**: You can check the balance of a wallet at any time. Example:

      .. code-block:: python

         balance = obj.wallet.balance

   e. **Transaction History**: Retrieve a wallet's transaction history. Example:

      .. code-block:: python

         transactions = obj.wallet.wallet_operations.all()

For more advanced usage and details on available methods and features, refer to the complete documentation.

Configuration
=============

If you need to customize the behavior of `django_advanced_wallet`, you can do so by adding the following settings to your project's `settings.py`:

- Preparing...
