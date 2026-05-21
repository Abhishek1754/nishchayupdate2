from .models import WalletTransaction


def create_wallet_transaction(

    user,
    transaction_type,
    source,
    amount,
    remark=""

):

    WalletTransaction.objects.create(

        user=user,

        transaction_type=transaction_type,

        source=source,

        amount=amount,

        balance_after=user.wallet_balance,

        remark=remark,

    )