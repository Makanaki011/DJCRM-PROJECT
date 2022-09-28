
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from leads.views import landing_page, Signupview
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name="landing-page"),
    path('leads/', include('leads.urls', namespace="leads")),
    path('agents/', include('agents.urls', namespace="agents")),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', Signupview.as_view(), name="signup"),
    path('reset-password/', PasswordResetView.as_view(), name="reset_password"),
    path('Password-rest-done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    

    # path('', include('leads.urls')),   
    # path('', landing_page),
     
      
   
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
