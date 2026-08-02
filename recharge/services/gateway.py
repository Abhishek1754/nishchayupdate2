from recharge.models import RechargeAPIConfiguration

from .finpay import FinPayGateway
from .fastpay import FastPayGateway
from .epay import EPayGateway


class RechargeGateway:

    @classmethod
    
    def process_recharge(

    cls,
    provider,
    mobile_number,
    amount,
    transaction_id

):
   

        config = RechargeAPIConfiguration.objects.first()
        service_type = provider.service_type

        if not config:
            raise Exception(
                "Recharge API Configuration not found."
            )

        if service_type == "mobile":

            if config.mobile_api == "FASTPAY":

                return FastPayGateway.recharge(

                    provider.fastpay_operator_code,
                    mobile_number,
                    amount,
                    transaction_id

                )

            elif config.mobile_api == "FINPAY":

                return FinPayGateway.recharge(

                    provider.operator_code,
                    mobile_number,
                    amount,
                    transaction_id

                )

        elif service_type == "dth":

            return EPayGateway.recharge(

                provider.operator_code,
                mobile_number,
                amount,
                transaction_id

            )

        raise Exception("Unsupported recharge type.")