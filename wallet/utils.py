from decimal import Decimal

from .models import WalletTransaction


# =====================================================
# CREATE WALLET TRANSACTION
# =====================================================

def create_wallet_transaction(

    user,
    transaction_type,
    source,
    amount,
    remark=""

):

    # =========================
    # SAFE DECIMAL CONVERSION
    # =========================

    amount = Decimal(amount)

    # =========================
    # CREATE TRANSACTION
    # =========================

    WalletTransaction.objects.create(

        user=user,

        transaction_type=transaction_type,

        source=source,

        amount=amount,

        balance_after=user.wallet_balance,

        remark=remark,

    )

    return True