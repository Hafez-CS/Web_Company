from django.apps import AppConfig


class TransactionModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions_module'

    def ready(self):
        import transactions_module.signals
