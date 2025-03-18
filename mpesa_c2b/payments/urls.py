from django.urls import path
from . import views

urlpatterns = [
    
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('refresh-token/', views.RefreshTokenView.as_view(), name = "Refresh token to get new tokens"),
    
    path('account/', views.AccountListView.as_view(), name='company-list-for the single user that we are using the jwt for.'),
    path('account/<str:unique_code>/', views.AccountRetrieveUpdateDeleteView.as_view(), name='company-detail, update, delete, modify.'),
    path('accountall/', views.AccountListall.as_view(), name='List all the company and id by also adding a param with the number of results we want'),
    
    path('account-type/', views.AccountTypeListCreateView.as_view(), name='account'),
    path('account-typeupdate/<int:id>/', views.AccountTypeRetrieveUpdateDeleteView.as_view(), name = "account"),
    
    path('gen/<path:extra_path>/', views.ProcessCallBackURLsView.as_view(), name='process_appended_url'),
    
    path('stk/', views.StkPush.as_view(), name='stk_push'),
    path('b2c/', views.B2CPayment.as_view(), name='stk_push'),
    path('c2b/', views.C2BPayment.as_view(), name='stk_push'),
    # View trasactions
    path('stk-transactions/', views.STKTransactionListView.as_view(), name='stk_push'),
    path('c2b-transactions/', views.C2BTransactionListView.as_view(), name='stk_push'),
    path('b2c-transactions/', views.B2CTransactionListView.as_view(), name='stk_push'),
    
    path('stk-transactions/<int:id>/', views.STKTransactionListView.as_view(), name='stk_push'),
    path('c2b-transactions/<int:id>/', views.C2BTransactionListView.as_view(), name='stk_push'),
    path('b2c-transactions/<int:id>/', views.B2CTransactionListView.as_view(), name='stk_push'),

]
"""
    path('stk_push/', views.stk_push, name='stk_push'),
    path('b2c/', views.b2c, name='b2c'),
    path("b2c_result/", views.b2c_result, name="b2c_result"),
    
    path("c2b_register/", views.c2b_register_urls, name="c2b_register"),
    
    path("c2b/dummy_validation/", views.dummy_validation, name="dummy_validation"),
    path("c2b/confirm/", views.c2b_confirm, name="c2b_confirm"),
    path("simulate_c2b/", views.simulate_c2b_payment, name="simulate_c2b"),



    
    #Html reders
    path('signup/', views.SignUpView.as_view(), name='signup-login'),
    path('login/', views.LoginView.as_view(), name='update-account'),
    path('account/', views.AccountView.as_view(), name='delete-account'),

"""