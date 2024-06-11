from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from home.models import Person
from home.serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator

@api_view(['GET', 'POST'])
def index(request):
    cousre = {
        'name' : 'Python',
        'learn' : ['Django', 'Django rest', 'FastApi', 'Flask'],
        'course_provider' : 'Scaler'
    }

    if request.method == 'POST':
        data = request.data
        print(data)

    return Response(cousre)

# creating crud api using API-View class
class PersonAPI(APIView) :
    permission_classes = [IsAuthenticated]  
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            data = Person.objects.all()
            page_num = request.GET.get('page', 1)
            page_size = 2
            paginator = Paginator(data, page_size)
            serializer = PeopleSerializer(paginator.page(page_num), many = True)
            print("Get all people method call")
            return Response(serializer.data)
        except Exception as e :
            return Response({"status" : False, "message" : "Invalid Page number"})
    
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid() :
            serializer.save()
            print("Create person method call")
            return Response(serializer.data)
    
        return Response(serializer.errors)
        
    
    def put(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data)
        if serializer.is_valid() :
            serializer.save()
            print("update-put person method call")
            return Response(serializer.data)

        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data, partial = True)
        if serializer.is_valid() :
            serializer.save()
            print("update-patch person method call")
            return Response(serializer.data)

        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'Message': 'Person Deleted'})

# creating a CRUD methods using api-view decorator
@api_view(['POST'])
def login(request) :
    data = request.data
    serializer = LoginSerializer(data = data)
    if serializer.is_valid():
        data = serializer.validated_data
        return Response({'message' : "Successgully logged in"})
    
    return Response(serializer.errors)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request) :

    # if request.method == 'GET':
        
    # elif request.method == 'POST':
       
    # elif request.method == 'PUT':
        
    # elif request.method == 'PATCH':
        
    # else :
    pass
        
    
# creating CRUD methods using Model view set

class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith == search)

        serializer = PeopleSerializer(queryset, many=True)
        return Response({"Status Code " : 200, "Data" : serializer.data}, status=HTTP_200_OK )    

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)  

        if not serializer.is_valid():
            return Response({'status': False, 'message': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response({'status': True, 'message': "User created successfully"}, status=HTTP_201_CREATED)
    
class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data) 
        # validate the data
        if not serializer.is_valid():
            return Response({'status': False, 'message': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        # authenticate the user based on data
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        # check whether user exist or not
        if not user:
            return Response({'status': False, 'message': "Invalid Credential"}, status=HTTP_400_BAD_REQUEST)
        
        # now save the token
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'status':True,
            'message' : " User Login",
            'token' : str(token)
        }, status=HTTP_201_CREATED)