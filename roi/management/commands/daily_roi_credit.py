from django.core.management.base import BaseCommand

from django.utils import timezone

from decimal import Decimal

from roi.models import (
    Investment,
    DailyROIIncome
)

from accounts.models import User


class Command(BaseCommand):

    help = 'Daily ROI Credit System'

    def handle(self, *args, **kwargs):

        today = timezone.now().date()

        investments = Investment.objects.filter(
            status='active'
        )

        total_credited = 0

        for investment in investments:

            # =========================
            # CHECK MATURITY
            # =========================

            if investment.end_date.date() < today:

                investment.status = 'completed'

                investment.save()

                continue

            # =========================
            # DUPLICATE CHECK
            # =========================

            already_credited = DailyROIIncome.objects.filter(

                investment=investment,

                created_at__date=today

            ).exists()

            if already_credited:

                continue

            # =========================
            # DAILY ROI
            # =========================

            daily_income = investment.daily_income

            user = investment.user

            # =========================
            # CREDIT ROI WALLET
            # =========================

            user.roi_wallet += daily_income

            user.wallet_balance += daily_income

            user.total_earnings += daily_income

            user.save()

            # =========================
            # UPDATE INVESTMENT
            # =========================

            investment.total_earned += daily_income

            investment.save()

            # =========================
            # SAVE HISTORY
            # =========================

            DailyROIIncome.objects.create(

                investment=investment,

                user=user,

                amount=daily_income

            )

            total_credited += 1

            self.stdout.write(

                self.style.SUCCESS(

                    f"ROI Credited: {user.email} - ₹{daily_income}"

                )

            )

        self.stdout.write(

            self.style.SUCCESS(

                f"\nTOTAL ROI CREDITED: {total_credited}"

            )

        )