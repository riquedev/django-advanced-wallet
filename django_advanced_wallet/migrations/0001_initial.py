# Generated by Django 4.0.6 on 2022-08-02 02:05

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django_advanced_wallet.models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(default=django_advanced_wallet.models.get_wallet_id, max_length=12, primary_key=True, serialize=False, verbose_name='Wallet id')),
                ('balance', models.DecimalField(db_index=True, decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Balance')),
                ('previous_balance', models.DecimalField(db_index=True, decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Previous balance')),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': "Wallet's",
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WalletOperation',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(default=django_advanced_wallet.models.get_operation_id, max_length=15, primary_key=True, serialize=False, verbose_name='Operation id')),
                ('name', models.CharField(default='Wallet Operation', max_length=360, verbose_name='Operation name')),
                ('description', models.TextField(blank=True, verbose_name='Operation description')),
                ('value', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Operation value')),
                ('previous_value', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Previous wallet value')),
                ('cancel', models.BooleanField(db_index=True, default=False, verbose_name='Operation cancel')),
                ('cancel_cause', models.TextField(blank=True, verbose_name='Operation cancel cause')),
                ('operation_type', models.CharField(choices=[('DT', 'Deposit'), ('WD', 'Withdraw'), ('TO', 'Transfer Origin'), ('TD', 'Transfer Destination')], max_length=2)),
                ('object_id', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('post_cancel_operation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wallet_post_cancel_operation', related_query_name='wallet_post_cancel_operation', to='django_advanced_wallet.walletoperation', verbose_name='Post cancellation operation')),
                ('related_operation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wallet_related_operations', related_query_name='wallet_related_operations', to='django_advanced_wallet.walletoperation', verbose_name='Related operation')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_operations', related_query_name='wallet_operations', to='django_advanced_wallet.wallet', verbose_name='Wallet')),
            ],
            options={
                'verbose_name': 'Operation',
                'verbose_name_plural': 'Operations',
                'abstract': False,
            },
        ),
    ]
