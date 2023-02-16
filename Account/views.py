from django.shortcuts import render
from Account.authtoken import get_tokens_access_for_user, get_tokens_for_user
from Account.models import *
from Account.serializers import CategorySerializer, ChangePasswordSerializer, ForgotPasswordSerializer, LoginSerializer, ProductBulkUploadSerializer, ProductSerializer, ProductupdeleteSerializer, ProfileSerializer, RegisterSerializer, UserdetailsSerializer, UserlistSerializer
from rest_framework import generics,status,permissions
# Create your views here.
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.parsers import *
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser



class Registration(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        try:
            serializer_data = self.serializer_class(data=request.data)
            if serializer_data.is_valid():
                serializer_data.save()
                context={'status':True,'message':"User Added Successfully"}
            else:
                context={'status':False,'message':serializer_data.errors}
            return Response(context,status=status.HTTP_200_OK)
        except Exception as e:
            context={'status':False,'message':"Something went wrong"}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
     
class Userlist(generics.ListAPIView):
        serializer_class = UserlistSerializer
        def get_queryset(self):
            
            try:
                data = UserMaster.objects.all()
            
                return data
            except Exception as e:
                context={'status':False,'message':"Something went wrong"}
                return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
class Login(generics.GenericAPIView):
    serializer_class= LoginSerializer
    def post(self,request):
        userdata=UserMaster.objects.filter(username=request.data.get("username")).last()
        serializer_data = self.serializer_class(data = request.data)
        if serializer_data.is_valid():
            access_token = get_tokens_for_user(userdata)
            refresh_token = get_tokens_access_for_user(userdata)
            
            data = UserdetailsSerializer(userdata).data
            context = {'status': True,'message': 'Login Successfully','data': data,"token":access_token,"refreshtoken":refresh_token}
            return Response(context, status=status.HTTP_200_OK)
        else:
            
            context = {'data':{'status': False,'message': serializer_data.errors}}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
      
class UserProfile(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        try :          
            user = UserMaster.objects.filter(id=request.user.id).last()
            serializer = self.serializer_class(user,many=False)
            context = {'status': True,'message': 'Data found successfully','data':serializer.data}
            return Response(context, status=status.HTTP_200_OK)
                
        except Exception as e:
            context = {'status': False, 'message': str(e)}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

class ChangePassword(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def patch(self,request):
        try:
            serializer = self.serializer_class(data=request.data,context={"userid":self.request.user.id})
            if serializer.is_valid():
                                                    
                context = {'status': True,'message': 'Password has been updated successfully.'}
                return Response(context, status=status.HTTP_200_OK)
            
            context = {'status': False,'message': serializer.errors['error'][0]}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False, 'message': str(e)}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ForgotPassword(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            context = {'status': True,'message': ' successfully.'}
            return Response(context, status=status.HTTP_200_OK)
        
        context = {'status': False,'message': serializer.errors}
        return Response(context, status=status.HTTP_200_OK)
   
   
class Categorylist(generics.ListAPIView):
        serializer_class = CategorySerializer
        def get_queryset(self):
            
            try:
                data = Category.objects.all()
            
                return data
            except Exception as e:
                context={'status':False,'message':"Something went wrong"}
                return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            

class Productlist(generics.ListAPIView):
        serializer_class = ProductSerializer
        def get_queryset(self):
            
            try:
                data = Product.objects.all()
            
                return data
            except Exception as e:
                context={'status':False,'message':"Something went wrong"}
                return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
class ProductUpdatedelete(generics.GenericAPIView):
    serializer_class=ProductupdeleteSerializer
    def patch(self,request,id):
        item = Product.objects.filter(id=id).last()
        serializer_data = self.serializer_class(item,data=request.data,partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            
            context = {'status': True,'message': ' successfully.'}
            return Response(context, status=status.HTTP_200_OK)
        
        context = {'status': False,'message': serializer_data.errors}
        return Response(context, status=status.HTTP_200_OK)
   
    def delete(self,request):
        item = Product.objects.filter(id=id).last()
        pass
    
    

class ProductUploadCSV(generics.GenericAPIView):
    serializer_class = ProductBulkUploadSerializer
    parser_classes = (FormParser, MultiPartParser)
    def post(self,request ,format=None):
        
        print(request.data)
        return Response("hello world")