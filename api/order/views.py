from django.shortcuts import render
from .serializers import OrderSerializer
from .models import Order
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all().order_by('id')
    serializer_class = OrderSerializer

def validate_user_session(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False

@csrf_exempt
def add(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid login  (ﾉಥ益ಥ）ﾉ'})

    if request.method == "POST":
        user_id = id
        transaction_id = request.POST['transaction_id']
        amount = request.POST['amount']
        products = request.POST['products']

        total_pro = len(products.split(',')[:-1])

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({'error': 'User does not exist please login |ಠ_ಠ|'})

        ordr = Order(user=user, product_name=products, total_products=total_pro,
                     transaction_id=transaction_id, total_amount=amount)
        ordr.save()
        return JsonResponse({'success': True, 'error': False, 'message': 'Your order have beeb successfully placed. Thank you!!! └(^o^ )\/( ^o^)┘'})