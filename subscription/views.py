from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import SubscriptionPlan


@api_view(['GET'])
def get_plan(request):
    user = request.user
    days = (timezone.now() - user.date_joined).days

    plan = SubscriptionPlan.objects.filter(
        days_from__lte=days,
        days_to__gte=days
    ).first()

    return Response({"price": plan.price if plan else 0})