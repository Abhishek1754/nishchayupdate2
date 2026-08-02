import requests


class FinPayGateway:

    BASE_URL = "https://ultra.myfinpaypro.co.in/api/Service/Recharge2"

    API_TOKEN = "b12418e1-7d26-4c68-b968-d2a0a368f082"

    @classmethod
    def recharge(
        cls,
        provider_code,
        mobile_number,
        amount,
        transaction_id
    ):

        url = (
            f"{cls.BASE_URL}?"
            f"ApiToken={cls.API_TOKEN}"
            f"&MobileNo={mobile_number}"
            f"&Amount={amount}"
            f"&OpId={provider_code}"
            f"&RefTxnId={transaction_id}"
        )

        headers = {
            "User-Agent": "curl/8.5.0",
            "Accept": "*/*"
        }

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=30
            )

            print("================================")
            print("FINPAY REQUEST")
            print(url)
            print("--------------------------------")
            print("STATUS :", response.status_code)
            print(response.text)
            print("================================")

            try:
                data = response.json()
            except Exception:

                return {
                    "STATUS": "FAILED",
                    "MESSAGE": "Recharge API did not return JSON",
                    "RAW": response.text
                }

            return cls.convert_response(data)

        except Exception as e:

            return {
                "STATUS": "FAILED",
                "MESSAGE": str(e)
            }

    @staticmethod
    def convert_response(data):

        return {

            "STATUS": str(data.get("STATUS", "0")),

            "MESSAGE": data.get(
                "MESSAGE",
                "Recharge Failed"
            ),

            "OPTXNID": data.get(
                "OPTXNID"
            ),

            "RAW": data

        }