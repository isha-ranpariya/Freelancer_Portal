from api.models import User, Proposal, Project
from rest_framework import views
from api import serializers
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from api.serializers import *
from rest_framework.permissions import IsAuthenticated
from api.custom_permission import *
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # Add custom claims to the access token
    refresh['is_freelancer'] = user.is_freelancer
    refresh['is_client'] = user.is_client
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserLogin(views.APIView):
    def post(self, request, format=None):
        serializer = UserloginSerializer(data=request.data)
        print("serializer", serializer)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'data':'Login success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['username or password not a valid']}},
                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# dgdfgdfg    #    
class Userprofile(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, format=None):
        ser = UserProfileSerializer(request.user)
        return Response(ser.data, status=status.HTTP_200_OK)


class UserRegister(views.APIView):
    def post(self, request, format=None):
        serializer = UserregisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'Data':'User Registred'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProjectAPIView(views.APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['client'] = request.user
            instance = serializer.save()
            return Response({'data': f"'{instance.title}' project created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None, format=None):
        if id is not None:
            query = Project.objects.filter(id=id)
            serializer = ProjectSerializer(query, many=True)
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        query = Project.objects.all()
        serializer = ProjectSerializer(query, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)



class ProposalAPIView(views.APIView):
    permission_classes = [IsAuthenticated]  
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = CreateProposalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print("----",serializer,"----")
            serializer.validated_data['freelancer'] = request.user
            x = serializer.validated_data['project']
            serializer.validated_data['client']=x.client
            print("This Is X--->>>",x)
            serializer.save()
            return Response({'data': "Proposal sent successfully,"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None, format=None):
        if id is not None:
            query = Proposal.objects.filter(id=id)
            serializer = ProposalSerializer(query, many=True)
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        # query = Proposal.objects.filter(freelancer=request.user)
        query = Proposal.objects.all()
        serializer = ProposalSerializer(query, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)



class UserChangePassword(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, format=None):
        ser = ChangePassword(data=request.data, context = {'user':request.user})
        if ser.is_valid(raise_exception=True):
            return Response({'data':'Password Changed Successfully'}, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(views.APIView):
    def get(self, request, id=None, format=None):
        if id is not None:
            queryset=User.objects.filter(id=id)
            serializer_class=UserSerializer(queryset,many=True)
            return Response({'data':serializer_class.data},status=status.HTTP_200_OK)
        queryset = User.objects.all()
        serializer_class = UserSerializer(queryset,many=True)
        return Response({'data':serializer_class.data},status=status.HTTP_200_OK)