from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "Stw_App"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("marketplace", views.Marketplace.as_view(), name="marketplace"),
    # Cart/saved later items 

    path("view/cart", views.UserCart.as_view(), name="cart"),
    path("view/cart/item/add/<str:pk>", views.AddCartItem.as_view(), name="add_cart_item"),
    path("view/cart/item/remove/<str:pk>", views.RemoveCartItem.as_view(), name="remove_cart_item"),
    # Checkout
    path("view/cart/checkout", views.UserCheckout.as_view(), name="checkout"),

    path("view/saved_later", views.VisitLater.as_view(), name="saved_later"),
    path("view/saved_later/item/add/<str:pk>", views.AddVisitLater.as_view(), name="add_saved_later"),
    path("view/saved_later/item/remove/<str:pk>", views.RemoveVisitLater.as_view(), name="remove_saved_later"),
    # Products
    path("product/add", views.AddProduct.as_view(), name="add_product"),
    path("products/edit/<str:pk>", views.EditProduct.as_view(), name="edit_product"),
    path("product/remove/<str:pk>", views.RemoveProduct.as_view(), name="remove_product"),
    path("product/view/<str:pk>", views.ViewProduct.as_view(), name="view_product"),
    path("comment/remove/<str:pk>", views.RemoveComment.as_view(), name="remove_comment"),
    
    # Authentication login/logout, signup/signout
    path("user", views.User.as_view(), name="user_profile"),
    path("user/Orders", views.YourOrders.as_view(), name="your_orders"),
    path("user/login", views.UserLogin.as_view(), name="login"),
    path("user/logout", views.UserLogout.as_view(), name="logout"),
    path("user/signUp", views.UserSignUp.as_view(), name="signup"),

    # Profiles
    path("profile/<str:pk>", views.Profiles.as_view(), name="profile_page"),
    path("profile/<str:pk>/products", views.ProfileProducts.as_view(), name="profile_products"),
    path("profile/<str:pk>/feedback", views.ProfileFeedback.as_view(), name="profile_feedback"),

    # Paypal URL
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("view/cart/checkout/success", views.CheckoutSuccess.as_view(), name="checkout_success")
]