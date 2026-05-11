def distribute_income(user, amount):
    parent = user.referred_by
    level = 1

    while parent and level <= 6:
        parent.wallet_balance += amount * 0.01
        parent.save()
        parent = parent.referred_by
        level += 1