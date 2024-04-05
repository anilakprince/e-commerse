from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
import re
import random
import json

def session_token_generate(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)] + [str(i) for i in range(10)]) for _ in range(length)) #random.SystemRandom is used for cryptographic security purposes.

@csrf_exempt
def signin(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Send a post request with valid parameters only'})
    try:
        data = json.loads(request.body.decode())
        username = data.get("email", "")
        password = data.get("password", "")
 
        if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",username):
            return JsonResponse({'error':'Invalid Email Id'})
        
        if len(password)<3:
            return JsonResponse({'error':'password length  should be greater than 3 characters'})
        
        UserModel=get_user_model()

        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                usr_dict=UserModel.objects.filter(email=username).values().first()
                usr_dict.pop('password')

                if user.session_token != "0":
                    user.session_token = "0"
                    user.save()
                    return JsonResponse({'error':'previous session exists...'})
                
                token=session_token_generate()
                user.session_token=token
                user.save()
                login(request,user)
                return JsonResponse({'token':token,'user':usr_dict})
            else:
                return JsonResponse({'error':'Invalid Password'})

        except UserModel.DoesNotExist:
                return JsonResponse({'error':'Invalid Email'})

    except json.JSONDecodeError:
        return JsonResponse({'error':'invalid json data'})


def signout(request, id):
    logout(request)
    UserModel = get_user_model()

    user = UserModel.objects.get(pk=id)
    user.session_token = "0"
    user.save()

    return JsonResponse({'success': 'Logout success'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create':[AllowAny]}

    queryset=CustomUser.objects.all().order_by('id')
    serializer_class= UserSerializer
    #register user
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Automatically log in the user after registration
            login(request, user)

            # Generate and set session token
            token = session_token_generate()
            user.session_token = token
            user.save()

            return Response({'token': token, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        action =self.action

        if action in self.permission_classes_by_action:
            return [permission() for permission in self.permission_classes_by_action[action]]
        else:
            return[AllowAny()]