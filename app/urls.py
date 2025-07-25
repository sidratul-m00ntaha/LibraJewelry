from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MypasswordChangeForm, mySetPasswordForm
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

urlpatterns = [
    # Main pages
    path("", views.home),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    # Product & category views
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),

    # User profile & address
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("updateAddress/<int:pk>/", views.UpdateAddress.as_view(), name="updateAddress"),

    # Cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="addtocart"),
    path("checkout/", views.checkout.as_view(), name="checkout"),
    path('search/', views.search, name='search'),

    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),

    # User authentication
    path("registration/", views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path("accounts/login/", auth_view.LoginView.as_view(
        template_name="app/login.html",
        authentication_form=LoginForm
    ), name="login"),

    path("passwordchange/", auth_view.PasswordChangeView.as_view(
        template_name="app/changepassword.html",
        form_class=MypasswordChangeForm
    ), name="passwordchange"),

    path("passwordchangedone/", auth_view.PasswordChangeDoneView.as_view(
        template_name="app/passwordchangedone.html"
    ), name="passwordchangedone"),

    path("logout/", CustomLogoutView.as_view(next_page="login"), name="logout"),
    path('wishlist/', views.wishlist_view, name='wishlist'),

    # Password reset
    path("password-reset/", auth_view.PasswordResetView.as_view(
        template_name="app/password_reset.html",
        form_class=MyPasswordResetForm
    ), name="password_reset"),

    path("password-reset/done/", auth_view.PasswordResetDoneView.as_view(
        template_name="app/password_reset_done.html"
    ), name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(
        template_name="app/password_reset_confirm.html",
        form_class=mySetPasswordForm
    ), name="password_reset_confirm"),

    path("password-reset-complete/", auth_view.PasswordResetCompleteView.as_view(
        template_name="app/password_reset_complete.html"
    ), name="password_reset_complete"),
]

# Serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
