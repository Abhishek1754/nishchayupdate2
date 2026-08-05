import requests


class EPayGateway:

    BASE_URL = "https://www.epayyatra.com/webservices/api/recharge"

    USERNAME = "9594777373"

    API_TOKEN = "Zb9VtxsJQ6yNbAFyuzXLl882UEEBNs"

    @classmethod
    def recharge(
        cls,
        provider_code,
        mobile_number,
        amount,
        transaction_id
    ):

        params = {

            "username": cls.USERNAME,

            "api_token": cls.API_TOKEN,

            "number": mobile_number,

            "amount": float(amount),

            "operator": provider_code,

            "ref_id": transaction_id,

        }

        try:

            response = requests.get(

                cls.BASE_URL,

                params=params,
                
                headers={
        "Accept": "application/json"
            },

                timeout=60

            )

            print("================================")
            print("EPAY REQUEST")
            print(params)
            print("--------------------------------")
            print("STATUS :", response.status_code)
            print(response.text)
            print("================================")
            
            try:
                data = response.json()
            except Exception:
                return {
                    "STATUS": "FAILED",
                    "MESSAGE": response.text
                    }
            return cls.convert_response(data)
            
                      

        except Exception as e:

            return {

                "STATUS": "FAILED",

                "MESSAGE": str(e)

            }

    @staticmethod
    def convert_response(data):

        status = str(
            data.get("status", "")
        ).lower()

        if status == "accepted":

            api_status = "2"

        elif status == "pending":

            api_status = "2"

        elif status == "success":

            api_status = "1"

        elif status == "refunded":

            api_status = "0"

        else:

            api_status = "0"

        return {

            "STATUS": api_status,

            "MESSAGE": data.get(

                "message",

                "Recharge Failed"

            ),

            "OPTXNID": data.get(

                "txn_id"

            ),

            "RAW": data

        }