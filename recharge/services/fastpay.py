import requests


class FastPayGateway:

    BASE_URL = "https://myfastpay.in/api/v1"

    API_TOKEN = "iqOGh6zfg8cebx2edPvGvG7XWVfCCL"

    @classmethod
    def recharge(

        cls,
        provider_code,
        mobile_number,
        amount,
        transaction_id

    ):

        url = f"{cls.BASE_URL}/recharge"

        headers = {

            "Authorization": f"Bearer {cls.API_TOKEN}",

            "Accept": "application/json",

            "Content-Type": "application/json"

        }

        payload = {

            "client_ref": transaction_id,

            "number": mobile_number,

            "provider_id": provider_code,

            "amount": float(amount)

        }

        try:

            response = requests.post(

                url,

                json=payload,

                headers=headers,

                timeout=60

            )

            print("================================")
            print("FASTPAY REQUEST")
            print(payload)
            print("--------------------------------")
            print("STATUS :", response.status_code)
            print(response.text)
            print("================================")

            data = response.json()

            return cls.convert_response(data)

        except Exception as e:

            return {

                "STATUS": "FAILED",

                "MESSAGE": str(e)

            }

    @staticmethod
    def convert_response(data):

        if not data.get("success"):

            return {

                "STATUS": "FAILED",

                "MESSAGE": data.get(
                    "message",
                    "Recharge Failed"
                )

            }

        recharge = data.get("data", {})

        status = recharge.get(
            "status",
            ""
        ).lower()

        if status == "success":

            api_status = "1"

        elif status == "pending":

            api_status = "2"

        else:

            api_status = "0"

        return {

            "STATUS": api_status,

            "MESSAGE": recharge.get(

                "message",

                data.get("message")

            ),

            "OPTXNID": recharge.get(

                "txnid"

            ),

            "RAW": data

        }