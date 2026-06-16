from decimal import Decimal

from .models import (

    SmartShareSetting,

    SmartShareTransaction,

)

def distribute_smart_share(user):

    if user.is_subscription_active:

        plan_type = 'paid'

    else:

        plan_type = 'free'

    current_user = user.referred_by

    level = 1

    while current_user and level <= 5:

        setting = SmartShareSetting.objects.filter(

            plan_type=plan_type,

            level=level,

            is_active=True

        ).first()

        if setting:

            current_user.wallet_balance += Decimal(

                setting.rupee_reward

            )

            current_user.nishchay_coin += (

                setting.coin_reward

            )

            current_user.save()

            SmartShareTransaction.objects.create(

                receiver=current_user,

                trigger_user=user,

                level=level,

                rupee_amount=setting.rupee_reward,

                coin_amount=setting.coin_reward,

            )

        current_user = current_user.referred_by

        level += 1