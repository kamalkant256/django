import json
from Account.models import Category, Product, UserMaster
from Account.utils import forgot_mail
from rest_framework import serializers
from django.contrib.auth.hashers import make_password,check_password
from django.core.validators import FileExtensionValidator
import pandas as pd

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = "__all__"
    
    def validate(self,attrs):
        username = attrs.get("username")
        first_name=attrs['first_name']
        last_name=attrs['last_name']
        email=attrs['email']
        
        password=attrs['password']
        
        attrs['raw_password'] = password
        attrs['password'] = make_password(password)
        
        # email = attrs.get("email")
        # first_name = attrs.get("first_name")
        # last_name = attrs.get("last_name")
        
        checkuser = UserMaster.objects.filter(username = username).last()
        
        if checkuser:
            raise serializers.ValidationError("user already exists")
        if (first_name or last_name or email) is None:
            raise serializers.ValidationError({"error":" first_name or last_name or email is mandatory"})
        
        
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
   
    def validate(self, attrs):
            
        if attrs.get('new_password') != attrs.get('confirm_new_password'):
            raise serializers.ValidationError({"error":"Passwords don't match."})
        print(self.context.get('userid'))
        user = UserMaster.objects.get(id=self.context.get('userid'))
     
        check_pass = check_password(attrs.get('new_password'),user.password)
        if check_pass == True:
            raise serializers.ValidationError({"error":"you cannot use current password"})
       
        user = UserMaster.objects.filter(id=self.context.get('userid')).update(password = make_password(attrs.get('confirm_new_password')))
        

        return super().validate(attrs)
       
       
class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    def validate(self,attrs):
        data = UserMaster.objects.filter(username = attrs.get('username')).last()
        if data is None:
            raise serializers.ValidationError("username is not valid")
        
        forgot_mail(data)        
        
        
        
        return super().validate(attrs)
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Product
        fields = ['id','name','category','quantity']
        
    def get_category(self,obj):
        return obj.category.name

    def get_quantity(self,obj):
        return obj.size.name
    
class ProductupdeleteSerializer(serializers.ModelSerializer):
     class Meta:
        model = Product
        fields ="__all__"

class ProductBulkUploadSerializer(serializers.ModelSerializer):
    filename = serializers.FileField(validators=[FileExtensionValidator( ['CSV',] ) ])
    class Meta:
            model = Product
            fields =['filename']
    def validate(self,attrs):
        print(attrs.get('filename'),'aaaaaaaaaaaaaaa')
        data = pd.read_csv(attrs.get('filename'))
        df_to_json = data.to_json(orient="records")
       
        df_to_json = json.loads(df_to_json)
        
    
            
        
        for row in df_to_json:
            row['name'] = str(row['name'])
            row['size_id'] = str(row['size_id'])
            row['category_id'] = str(row['category_id'])
            print(Product.objects.filter(name__iexact=row['name']),'dbjsvrfhuvsfuwy')
            productname = Product.objects.filter(name__iexact=row['name']).last()
        
            if not productname:
                data = Product()
                data.name=row['name']
                data.size_id = row['size_id']
                data.category_id = row['category_id']
                data.save()
            
            else:
                
                Product.objects.filter(name=row['name']).update(name=row['name'],size_id=row['size_id'],category_id=row['category_id'])
        
        
        return super().validate(attrs)
