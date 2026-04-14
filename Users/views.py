from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from backend import Users
from .serializers import SignupSerializer, LoginSerializer
import requests as http_requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from chat.api_keys import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

# Create your views here.
@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save() # takes the validated_data and create a new user in the database using the create method in the SignupSerializer  
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message' : "Signup Successfully",
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            request,
            username=serializer.validated_data['email'], # validated_data => contains the cleaned and validated input data,is available only after calling [serializer.is_valid()] => must return true to access it 
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message' : "Login Successfully",
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_with_google(request):

    code = request.data.get('code')

    if not code:
        return Response({'error': 'Code is required'}, status=400)
    token_response = http_requests.post(
        'https://oauth2.googleapis.com/token', 
        data={
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        })

    if token_response.status_code != 200:
        return Response({'error': 'Failed to obtain token'}, status=400)

    token_data = token_response.json()
    id_token_str = token_data.get('id_token')

    if not id_token_str:
        return Response({'error': 'ID token not found'}, status=400)

    try:
        user_info = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
    except Exception:
        return Response({'error': 'Invalid Google token'}, status=400)

    email = user_info.get('email')
    if not email:
        return Response({'error': 'Email not provided by Google'}, status=400)
    if not user_info.get('email_verified'): # Ensure the user's email is verified by Google to prevent fake or unconfirmed accounts from accessing the system
        return Response({'error': 'Email not verified'}, status=400)
    name = user_info.get('name', '')

    user, created = Users.objects.get_or_create(
        email=email,
        defaults={
            'username': email,
            'first_name': name.split()[0] if name else '',
            'last_name': name.split()[-1] if len(name.split()) > 1 else '',
        }
    )

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'message': 'Login Successfully',
        'is_new_user': created,
    })