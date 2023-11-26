from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from paypal.standard.forms import PayPalPaymentsForm

from .forms import *
from .mixins import *

from statistics import mean 

import uuid


class Home(TemplateView):
    # takes the template and renders the template
    
    template_name = "Stw_App/home.html"

    def get(self, request):
        return render(request, self.template_name)
    

class Marketplace(TemplateView,ProductRatingMixin):
    # takes the template and has variables saved to access some model objects, and a condition which manipulates the model object being returned in the context
    
    template_name = "Stw_App/marketplace.html"
 
    def get(self,request):

        # 41-45, gets all Candy objects in the model, stores all the Candy brands in a array uniquely
        all_candies = Candy.objects.all()
        brands = []
        for candy in all_candies:
            brands.append(candy.brand)

        query = self.request.GET.get("search")
        if query and query != "None":
            candy = Candy.objects.filter(Q(brand__icontains=query) | Q(candy_name__icontains=query) | Q(candy_description__icontains=query))
        else:
            candy = self.get_products_rating(request, Candy.objects.all().order_by("-id"))
        # Pagination Process with built in method
        candy = Paginator(candy, 5)
        page_number = request.GET.get("page", 1)
        try:
            page = candy.page(page_number)
        except:
            page = candy.page(1)
            messages.error(request, "The page you tried accessing does not exist!")
        context = {"candy": page,
                   "page_number" : page_number,
                   "query" : query,
                   "brands" : set(brands)}
        
        return render(request, self.template_name, context)
    
    
class AddProduct(LoginRequiredMixin,TemplateView):
    # GET - takes the template and gets the form and renders the template with the form 
    # POST - gets the form and the image field filled out and checks for form validation, if condition is false, return a flash message and return the "completed" form, if condition is true
    # add uncompleted values such as the seller which default should be the request.user, the default candy rating to be 0 and the rating of the product to be 0 and save and redirect to market
    # Both GET and POST methods must need the request.user to be authenticated or in other words logged in
    
    template_name = "Stw_App/add_product.html"
    login_url = "Stw_App:login"

    def get(self,request):
        context = {"form": CandyForm}
        return render(request, self.template_name, context)
    
    def post(self,request):
        form = CandyForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # set the excluded values from the candy object
            product.seller = request.user
            product.candy_rating = 0
            product.package_weight_lbs = float(product.package_weight_lbs)
            product.save()
            return redirect("Stw_App:marketplace")
        else:
            messages.error(request, "Creation of a product is unsuccessful, please try again later.")
            context = {"form" : form}
            return render(request, self.template_name, context)


class EditProduct(LoginRequiredMixin, UpdateView):
    # Must be logged in, able to update a modelform object with these built in variables
    
    login_url = "Stw_App:login"
    template_name = "Stw_App/edit_product.html"

    model = Candy
    form_class = CandyForm
    success_url = reverse_lazy("Stw_App:marketplace")


class ViewProduct(TemplateView, ProductRatingMixin):
    # GET - get the product as well as the product ratings with the ProductRatingMixin from mixins.py. Check for queries, if query was made for comments, then show comments which the title
    # or description icontains the query which means incase sensitive. create a context with these variables we made and render it out with these variables
    # POST - get the candy object and the filled out comment form and check if its valid and automate the uncompleted hidden values such as the connected product to the comment and the user
    # and save the comment object with a success message along redirecting the user to the same path
    
    template_name = "Stw_App/view_product.html"
    form = CandyCommentForm()

    def get(self,request, pk):
        try:
            product = self.get_products_rating(request, get_object_or_404(Candy, id=pk))
        except:
            messages.error(request, "Product Not Avaliable, Sorry!")
            return redirect("Stw_App:marketplace")
        query = self.request.GET.get("search")
        comments = CandyComment.objects.filter(candy_product=product).filter(Q(title__icontains=query) | Q(comment__icontains=query)).order_by("-id") if query else CandyComment.objects.filter(candy_product=product).order_by("-id")
        context = {
            "product" : product,
            "form" : self.form,
            "comments" : comments,
            "query" : query
        }
        return render(request, self.template_name, context)
    
    def post(self,request,pk):
        product = get_object_or_404(Candy, id=pk)
        form = CandyCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.candy_product = product
            comment.save()
            messages.success(request, "Comment added successfully")
        return HttpResponseRedirect(f"{self.request.path_info}#product-comments")
    
class RemoveProduct(LoginRequiredMixin, View):
    # GET - get the product we want to remove, before removing anything, check to make sure once again the request.user meaning the user of the request and the product seller match and if
    # it is not true instantly redirect user back to the marketplace, we don't need to write an else statment because there is a return statment meaning that if the condition is true,
    # run that specific line of code which is a return call which means no other lines of code will run after that. .delete() call to delete an object, return flash message and redirect
    
    login_url = "Stw_App:login"

    def get(self,request, pk):
        product = get_object_or_404(Candy, id=pk)
        if request.user != product.seller:
            return redirect("Stw_App:marketplace")
        product.delete()
        messages.success(request, "Product was removed successfully")
        return redirect("Stw_App:marketplace")


class RemoveComment(LoginRequiredMixin, View):
    # GET - same thing as above, get the comment we want to remove and before removing anything make sure the current request.user is equal to the comment.user, HINT: look at models to see
    # the method we can call from the model ex comment.method, if the request.user is equal to the comment.user proceed pass the if statment and call the delete method on the comment
    # flash message for a success and return to the previous page
   
    login_url = "Stw_App:login"

    def get(self,request,pk):
        comment = get_object_or_404(CandyComment, id=pk)
        if request.user != comment.user:
            messages.error(request, "Error 404 while removing comment")
            return HttpResponseRedirect(self.request.path_info)
        comment.delete()
        messages.success(request, "Comment was removed successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddCartItem(LoginRequiredMixin,View):
    # GET - Must be logged in, will not render a template, but when it loads that specific page, get the product the user wants to add, make sure that the product is in stock and create a
    # cartobject object yes horrible wording but whatever and return a success message with a redirecto the actual cart
    
    login_url = "Stw_App:login"
    
    def get(self, request, pk):
        product = get_object_or_404(Candy, id=pk)

        if not product.in_stock: 
            return redirect("Stw_App:marketplace")
        
        add_product = CartObject.objects.create(item=product, linked_user=request.user)
        messages.success(request, "One product has been successfully added to your Shopping Cart.")
        return redirect("Stw_App:cart")


class RemoveCartItem(LoginRequiredMixin, View):
    # GET - get the cart object and use the delete method on the specific cart object, and return a flash message back to the user and redirect the user to the same page
    
    login_url = "Stw_App:login"

    def get(self,request,pk):
        product = get_object_or_404(CartObject, id=pk)
        product.delete()
        messages.success(request, "One product has been successfully removed from your Shopping Cart.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserCart(LoginRequiredMixin,TemplateView, CartMixin):
    # render out the template and get the context from the CartMixin method called get_cart_values, view mixins.py to see more
   
    template_name = "Stw_App/your_cart.html"
    login_url = "Stw_App:login"

    def get(self, request):
        context = self.get_cart_values(request)
        return render(request, self.template_name, context)

class UserCheckout(LoginRequiredMixin, TemplateView, CartMixin):
    template_name = "Stw_App/checkout.html"
    login_url = "Stw_App:login"

    def get(self,request):
        context = self.get_cart_values(request)
        if len(context["cart"]) < 1:
            messages.error(request, "An error has occured, please try again.")
            return redirect("Stw_App:cart")
        host = request.get_host()

        paypal_checkout = {
            "business" : settings.PAYPAL_RECEIVER_EMAIL,
            "amount" : context["total"],
            "item_name" : context["cart"],
            "invoice" : uuid.uuid4(),
            "currency_code" : "USD",
            "notify_url" : f"http://{host}/paypal/",
            "return_url" : f"http://{host}/view/cart/checkout/success",
            "cancel_url" : f"http://{host}/view/cart",
        }
        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        paypal_context = {"paypal_payment" : paypal_payment}
        merged_context = {**context, **paypal_context}

        return render(request, self.template_name, {**merged_context, "paypal": paypal_payment})

class CheckoutSuccess(LoginRequiredMixin, View):
    def get(self,request):
        http_request = request.get_full_path()
        if "PayerID" in http_request:
            cart_items = CartObject.objects.filter(linked_user = request.user).order_by("-id")
            for cart_item in cart_items:
                PurchasedObject.objects.create(item = cart_item.item, linked_user = request.user)
                cart_item.delete()
            return redirect("Stw_App:your_orders")
        else:
            messages.error(request, "An error has occured, please try again later.")
            return redirect("Stw_App:cart")

class YourOrders(LoginRequiredMixin, TemplateView):
    template_name = "Stw_App/your_orders.html"
    login_url = "Stw_App:login"

    def get(self,request):
        ordered_products = PurchasedObject.objects.filter(linked_user = request.user).order_by("-id")
        context = {"ordered_products" : ordered_products}
        return render(request, self.template_name, context)
    
class AddVisitLater(LoginRequiredMixin,View):
    # No template gets rendered out, just complete logic, gets the product, creates a object using the model SavedLaterObjects and returns a success message and redirects user to the
    # visit later or saved later page

    login_url = "Stw_App:login"

    def get(self,request, pk):
        product = get_object_or_404(Candy, id=pk)

        add_product = SavedLaterObject.objects.create(linked_user=request.user, item = product)
        messages.success(request, "One product has been successfully added to your Saved Items.")
        return redirect("Stw_App:saved_later")


class RemoveVisitLater(LoginRequiredMixin, View):
   # No template gets rendered out, gets the product a user wants to remove, and deletes that product and returns a flash message with a redirect to the saved later page

   login_url = "Stw_App:login"
   
   def get(self,request,pk):
        product = get_object_or_404(SavedLaterObject, id=pk)
        product.delete()
        messages.error(request, "One product has been successfully removed from your Saved Items.")
        return redirect("Stw_App:saved_later")
    

class VisitLater(LoginRequiredMixin, TemplateView):
    # The actual page with all the saved later items a user can save. Filter through the SavedLaterObject's model and filter it so it only shows the current users 
    # saved later products and assign it to a variable and render out that variable which should be an array of objects you can iterate over

    template_name = "Stw_App/saved_later.html"
    login_url = "Stw_App:login"

    def get(self, request):
        saved_later = SavedLaterObject.objects.filter(linked_user = request.user).order_by("-id")
        context = {"saved_later" : saved_later}
        return render(request, self.template_name, context)
    

# Authentication 
class UserLogin(TemplateView):
    # GET - makes sure that user is actually not authenticated before allowing them to view the page, load the LoginForm() and render out the template
    # POST - get the form with the request data, call the method .is_valid() on the form, get the username and password from the form by the name of the inputs, try to authenticate
    # if all goes well, login the actual user else, show an error message

    template_name = "Stw_App/login.html"

    def get(self, request):
        # Checks if user is logged in already
        if request.user.is_authenticated :
            return redirect("Stw_App:marketplace")
        form = LoginForm()
        context = {"form" : form}
        return render(request, self.template_name, context)
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username_input")
            password = request.POST.get("password_input")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, "You've successfully logged in")
                return redirect("Stw_App:marketplace")
            else:
                messages.error(request, "Incorrect Username or Password.")
                return redirect("Stw_App:login")
        else:
            messages.error(request, "Please complete the reCAPTCHA to login")
            return redirect("Stw_App:login")


class UserLogout(LoginRequiredMixin, TemplateView):
    # 
    template_name = "Stw_App/logout.html"
    login_url = "Stw_App:login"

    def get(self,request):
        # Checks if user is logged in already
        if request.user.is_authenticated :
            return render(request, self.template_name)
        return redirect("Stw_App:marketplace")
    
    def post(self,request):
        logout(request)
        return redirect("Stw_App:marketplace")


class UserSignUp(TemplateView):
    # GET - same thing as UserLogin, checks if the user is logged in already, if so do not render this page and redirec tthe user, else render the page with the form
    # POST - get the form and if the form is valid, save the form and log in the user, if the form is not valid, run the custom sign up errors

    template_name = "Stw_App/SignUp.html"
    form = CreateUserForm()

    def get(self,request):
        # Checks if user is logged in already
        if request.user.is_authenticated :
            return redirect("Stw_App:marketplace")
        context = {
            "form": self.form
        }
        return render(request, self.template_name, context)
        
    def post(self,request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # Login The User Signed Up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            # Return success message
            messages.success(request, "Account Created Successfully")
            return redirect("Stw_App:marketplace")
        else:
            # Custom Sign Up Errors
            User = get_user_model()
            username = request.POST.get("username")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if len(password1) < 8 or len(password2) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
            elif password1 != password2:
                messages.error(request, "Passwords do not match.")
            elif User.objects.filter(username=username):
                messages.error(request, "Username is already in use.")
            elif not form.cleaned_data["captcha"]:
                messages.error(request, "Please complete the reCAPTCHA to login")
            else:
                messages.error(request, "Your password is too weak, please create a stronger password")
            return render(request, self.template_name, context={"form": form})


# Make user actually your own user control panel for your account
class User(TemplateView, ProfileMixin):
    # GET - Navbar item which when clicked shows information about YOU as a user, the products you created and feedback activity written to people, gets this information with the ProfileMixin

    template_name = "Stw_App/user.html"

    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("Stw_App:login")
        user = request.user
        context = self.get_user_details(request, user=user)
        return render(request, self.template_name, context)
    

class Profiles(TemplateView, ProfileMixin):
    # GET - same concept as above, but this time its with a specific profile using a primary key. Uses the same ProfileMixin to get the information about the user
    
    template_name = "Stw_App/user.html"

    def get(self,request,pk):
        User = get_user_model()
        user = get_object_or_404(User, id=pk)
        context = self.get_user_details(request,user=user)
        return render(request, self.template_name, context)
    
    
class ProfileProducts(TemplateView, ProfileMixin):
    # GET - same concept as above, instead whats different lies in the html where we show different things

    template_name = "Stw_App/user_products.html"

    def get(self, request, pk):
        User = get_user_model()
        user = get_object_or_404(User, id=pk)
        context = self.get_user_details(request,user=user)
        return render(request, self.template_name, context)
    

class ProfileFeedback(TemplateView, ProfileMixin):
    # GET - same concept as above, instead whats different lies in the html where we show different things 

    template_name = "Stw_App/user_feedback_given.html"

    def get(self, request, pk):
        User = get_user_model()
        user = get_object_or_404(User, id=pk)
        context = self.get_user_details(request,user=user)
        return render(request, self.template_name, context)