from django.urls import path,include

from Account.views import *

urlpatterns = [
    path('registration/',Registration.as_view(),name="registration"),
    path('userlist/',Userlist.as_view(),name="userlist"),   
    path('userprofile/',UserProfile.as_view(),name="userprofile"),
    path('login/',Login.as_view(),name="login"),
    path('changepassword/',ChangePassword.as_view(),name="changepassword"),
    path('forgotpassword/',ForgotPassword.as_view(),name="forgotpassword"),
    path('catlist/',Categorylist.as_view(),name="catlist"),   
    path('productlist/',Productlist.as_view(),name="productlist"),   
    path('productupdelete/<str:id>',ProductUpdatedelete.as_view(),name="productupdelete"),   
    path('bulkproductupload/',ProductUploadCSV.as_view(),name="bulkproductupload"),   
    
    
    
    
    
    
]
