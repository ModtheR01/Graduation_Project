from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from Users.models import User
from .serializers import SignupSerializer, LoginSerializer
import requests as http_requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from chat.api_keys import AUTH_GOOGLE_CLIENT_ID, AUTH_GOOGLE_CLIENT_SECRET, AUTH_GOOGLE_REDIRECT_URI
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password

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
                'fname' : user.fname,
                'lname' : user.lname,
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def user_info(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'email': user.email,
            'first_name': user.fname,
            'last_name': user.lname,
            'phone_number': user.phone_number,
            'country': user.country,
            'city': user.city,
            'street': user.street,
            'birth_date': user.birth_date,
        })
    return Response({'error': 'User not authenticated'}, status=401)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    user = request.user
    user.fname = request.data.get('fname', user.fname)
    user.lname = request.data.get('lname', user.lname)
    user.phone_number = request.data.get('phone_number', user.phone_number)
    user.country = request.data.get('country', user.country)
    user.city = request.data.get('city', user.city)
    user.street = request.data.get('street', user.street)
    user.birth_date = request.data.get('birth_date', user.birth_date)
    user.save()
    return Response({'message': 'User information updated successfully'})

@api_view(['POST'])
def login_with_google(request):

    code = request.data.get('code') # catch the authorization code sent by google after the user successfully authenticated with google, this code is a temporary token that can be exchanged for an access token and an ID token, which contain the user's information and can be used to authenticate the user in our system.

    if not code:
        return Response({'error': 'Code is required'}, status=400)
    token_response = http_requests.post(     # Send a POST request to Google's token endpoint to exchange the authorization code for tokens (access token and ID token). The request includes the authorization code, client ID, client secret, redirect URI, and grant type. The response will contain the tokens if the request is successful.
        'https://oauth2.googleapis.com/token', 
        data={
            'code': code,
            'client_id': AUTH_GOOGLE_CLIENT_ID,
            'client_secret': AUTH_GOOGLE_CLIENT_SECRET,
            'redirect_uri': AUTH_GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        })

    print(f"[Google Auth] token exchange status: {token_response.status_code}")
    if token_response.status_code != 200:
        print(f"[Google Auth] token exchange failed: {token_response.json()}")
        return Response({'error': 'Failed to obtain token'}, status=400)

    token_data = token_response.json()
    id_token_str = token_data.get('id_token')

    if not id_token_str:
        print("[Google Auth] id_token not found in response")
        return Response({'error': 'ID token not found'}, status=400)

    try:
        user_info = id_token.verify_oauth2_token( # check if is sent by google or not , and check if this token from my app(app created on google console) or from another app, if this checks passed it will return the user's information contained in the ID token, such as email and name, which can be used to create or authenticate the user in our system.
            id_token_str,
            google_requests.Request(),
            AUTH_GOOGLE_CLIENT_ID
        )
        print(f"[Google Auth] user verified: {user_info.get('email')}")
    except Exception as e:
        print(f"[Google Auth] error occurred: {e}")
        return Response({'error': 'Invalid Google token'}, status=400)

    email = user_info.get('email')
    if not email:
        print("[Google Auth] Email not provided by Google")
        return Response({'error': 'Email not provided by Google'}, status=400)
    if not user_info.get('email_verified'): # Ensure the user's email is verified by Google to prevent fake or unconfirmed accounts from accessing the system
        print("[Google Auth] Email not verified")
        return Response({'error': 'Email not verified'}, status=400)
    name = user_info.get('name', '')
    first_name=''
    last_name=''

    if name: # if the name not equal empty string
        parts_of_name = name.split() # split the full name into parts (e.g., first name and last name) based on spaces. This allows us to extract the first and last names from the full name provided by Google.
        first_name= parts_of_name[0] if len(parts_of_name) > 0 else ''
        last_name = parts_of_name[-1] if len(parts_of_name) > 1 else ''

    user, created = User.objects.get_or_create( # get_or_create returns two values: user = the user object (existing or newly created) , created = True if a new user was created, False if it already existed
        email=email, # to search for an existing user with the provided email. If a user with that email already exists, it will return that user and created will be False. If no user with that email exists, it will create a new user with the provided email and name, and created will be True.
        defaults={
            'fname': first_name,
            'lname': last_name,
        }
    )

    print(f"[Google Auth] user: {email} | created: {created}")
    if created:
        user.set_unusable_password() # Since the user is authenticated through Google, we set an unusable password to prevent login with a password. This ensures that the user can only authenticate using their Google account and not through traditional username/password authentication.
        user.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'message': 'Login Successfully',
        'is_new_user': created,
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'message': 'User account deleted successfully'})


@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "If this email exists, a reset link was sent."})

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_link = f"https://romee-lake.vercel.app/reset-password/{uid}/{token}/"

    send_mail(
        subject="Reset Your Password",
        message=f"Click here to reset your password:\n{reset_link}",
        from_email="romee.agent@gmail.com",
        recipient_list=[email],
    )

    return Response({"message": "If this email exists, a reset link was sent."})


@api_view(['POST'])
def reset_password(request):
    uid = request.data.get("uid")
    token = request.data.get("token")
    new_password = request.data.get("new_password")

    if not new_password or len(new_password) < 6:
        return Response({"error": "Password too weak"}, status=400)

    try:
        email = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(email=email)
    except Exception:
        return Response({"error": "Invalid link"}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=400)

    try:
        validate_password(new_password)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password reset successful"}, status=200)