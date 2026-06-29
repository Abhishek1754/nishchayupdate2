from rest_framework import serializers

from accounts.models import User

from .models import Shop


class ShopRegistrationSerializer(serializers.Serializer):

    # ==========================
    # USER DETAILS
    # ==========================

    owner_name = serializers.CharField()

    owner_email = serializers.EmailField()

    owner_contact = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    # ==========================
    # SHOP DETAILS
    # ==========================

    shop_name = serializers.CharField()

    shop_category = serializers.CharField()

    full_address = serializers.CharField()

    state = serializers.CharField()

    city = serializers.CharField()

    pincode = serializers.CharField()

    latitude = serializers.CharField(
        required=False,
        allow_blank=True
    )

    longitude = serializers.CharField(
        required=False,
        allow_blank=True
    )

    shop_contact = serializers.CharField()

    # ==========================
    # GST / PAN
    # ==========================

    gst_number = serializers.CharField(
        required=False,
        allow_blank=True
    )

    pan_number = serializers.CharField()

    business_pan = serializers.CharField(
        required=False,
        allow_blank=True
    )

    # ==========================
    # BANK DETAILS
    # ==========================

    bank_name = serializers.CharField()

    account_holder = serializers.CharField()

    account_number = serializers.CharField()

    ifsc_code = serializers.CharField()

    # ==========================
    # DOCUMENTS
    # ==========================

    aadhaar_front = serializers.ImageField()

    aadhaar_back = serializers.ImageField()

    pan_card = serializers.ImageField()

    business_pan_file = serializers.ImageField(
        required=False
    )

    shop_photo = serializers.ImageField()

    # ==========================
    # PLAN
    # ==========================

    subscription_type = serializers.ChoiceField(

        choices=[

            "free",

            "premium"

        ]

    )

    referral_code = serializers.CharField(
        required=False,
        allow_blank=True
    )

    # ==========================
    # VALIDATION
    # ==========================

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:

            raise serializers.ValidationError(

                "Password does not match."

            )

        if User.objects.filter(

            email=attrs["owner_email"]

        ).exists():

            raise serializers.ValidationError(

                "Email already registered."

            )

        if User.objects.filter(

            phone=attrs["owner_contact"]

        ).exists():

            raise serializers.ValidationError(

                "Mobile already registered."

            )

        return attrs