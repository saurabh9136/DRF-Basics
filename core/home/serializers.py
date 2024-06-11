from rest_framework import serializers
from .models import Person,Color
from django.contrib.auth.models import User

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if 'username' in data:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('Username already exists')
        
        if 'email' in data:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email already exists')
        
        return data
    
    def create(self, valid_data):
        user = User.objects.create(username = valid_data['username'], email = valid_data['email'] )
        user.set_password(valid_data['password'])
        user.save()
        return user

class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer() # serialize the data fetch only required fields 
    hex_code = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1 # fetch all data

    

    def validate(self, data):
        if data['age'] < 18 :
            raise serializers.ValidationError("You are not eligible")
        
        sp_char = "!@#$%^&*()<>,._+?/|\[]`~"
        if any(c in sp_char for c in data['name']):
            raise serializers.ValidationError("Name do not consist any special characters")
        
        return data
    
    def get_hex_code(self, obj):

        color_obj = Color.objects.get(id = obj.color.id)

        return {'color_name':color_obj.color_name, 'hex_code': '#0000'}