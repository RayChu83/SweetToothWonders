from django.urls import path, include
from . import views

app_name = "Stw_App"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("Marketplace", views.Marketplace.as_view(), name="marketplace"),
    # Cart/saved later items 

    path("View/Cart", views.UserCart.as_view(), name="cart"),
    path("View/Cart/Item/Add/<str:pk>", views.AddCartItem.as_view(), name="add_cart_item"),
    path("View/Cart/Item/Remove/<str:pk>", views.RemoveCartItem.as_view(), name="remove_cart_item"),
    # Checkout
    path("View/Cart/Checkout", views.UserCheckout.as_view(), name="checkout"),

    path("View/Saved_Later", views.VisitLater.as_view(), name="saved_later"),
    path("View/Saved_Later/Item/Add/<str:pk>", views.AddVisitLater.as_view(), name="add_saved_later"),
    path("View/Saved_Later/Item/Remove/<str:pk>", views.RemoveVisitLater.as_view(), name="remove_saved_later"),
    # Products
    path("Product/Add", views.AddProduct.as_view(), name="add_product"),
    path("Products/Edit/<str:pk>", views.EditProduct.as_view(), name="edit_product"),
    path("Product/Remove/<str:pk>", views.RemoveProduct.as_view(), name="remove_product"),
    path("Product/View/<str:pk>", views.ViewProduct.as_view(), name="view_product"),
    path("Comment/Remove/<str:pk>", views.RemoveComment.as_view(), name="remove_comment"),
    
    # Authentication login/logout, signup/signout
    path("User/", views.User.as_view(), name="user_profile"),
    path("User/Orders", views.YourOrders.as_view(), name="your_orders"),
    path("User/Login", views.UserLogin.as_view(), name="login"),
    path("User/Logout", views.UserLogout.as_view(), name="logout"),
    path("User/SignUp", views.UserSignUp.as_view(), name="signup"),

    # Profiles
    path("Profile/<str:pk>/", views.Profiles.as_view(), name="profile_page"),
    path("Profile/Products/<str:pk>/", views.ProfileProducts.as_view(), name="profile_products"),
    path("Profile/Feedback/<str:pk>/", views.ProfileFeedback.as_view(), name="profile_feedback"),

    # Paypal URL
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("View/Cart/Checkout/Success", views.CheckoutSuccess.as_view(), name="checkout_success")
]
