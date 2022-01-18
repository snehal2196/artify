from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.views import View
from django.contrib.auth import views as auth_views
from .forms import LoginForm, ChangePasswordForm, PasswordSetForm, ResetPasswordForm

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('paymentdone/',views.paymentdone,name='paymentdone'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class= ChangePasswordForm, success_url='/passwordchangedone/'),
    name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset',auth_views.PasswordResetView.as_view(template_name='app/resetpassword.html', form_class=ResetPasswordForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/resetpassworddone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/resetpasswordconfirm.html', form_class=PasswordSetForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/resetpasswordcomplete.html'),name='password_reset_complete'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topwear'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('shop/', views.shop, name='shop'),
    path('about/',views.about, name='about'),
    path('contact/',views.ContactView.as_view(), name='contact'),
    path('category/<slug:category>', views.category, name='category'),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)


# class CartSetting(admin.ModelAdmin):
#     list_display = ('id','user','product','quantity')

# admin.site.register(Cart,CartSetting)

# class OrderPlacedSetting(admin.ModelAdmin):
#     list_display = ('id','user','customer','product','quantity','ordered_date','status')

# admin.site.register(OrderPlaced,OrderPlacedSetting)