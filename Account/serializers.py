from Account.models import UserMaster
from rest_framework import serializers
from django.contrib.auth.hashers import make_password,check_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = "__all__"
    
    def validate(self,attrs):
        username = attrs.get("username")
        password=attrs['password']
        password=make_password(password)
        
        # email = attrs.get("email")
        # first_name = attrs.get("first_name")
        # last_name = attrs.get("last_name")
        
        checkuser = UserMaster.objects.filter(username = username).last()
        
        if checkuser:
            raise serializers.ValidationError("user already exists")
        
        else:
            UserMaster.objects.create(username=attrs['username'],password=password,email=attrs['email'],first_name=attrs['first_name'],last_name=attrs['last_name'])
        return super().validate(attrs)
            
        
class UserlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = ["id","username","email","first_name","last_name"]
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields ="__all__"
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=600,error_messages={'blank': 'Please enter email address'})
    password = serializers.CharField(max_length=600,error_messages={'blank': 'Please enter password'})
    
    def validate(self,attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        password=make_password(password)
        
        user_check = UserMaster.objects.filter(username = username).last()
        print(user_check,'aaaaaaaaaaaaaaaaaa')
        if user_check is None:
            print("nulll")
            raise serializers.ValidationError("Username can not be empty")
        if (not user_check.check_password(attrs.get("password"))):  
 
            print("data")
            raise serializers.ValidationError("password is wrong")
        
        return super().validate(attrs)

class UserdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields ="__all__"
        
        
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length = 30)
    new_password = serializers.CharField(max_length = 30)
    confirm_new_password = serializers.CharField(max_length = 30)
    
    def validate(self,attrs):
        pass
    
    
