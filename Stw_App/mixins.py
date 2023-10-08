from .models import *
from statistics import mean 

class ProductRatingMixin():
    def get_products_rating(self,request,product):
        # Try Except call for conditions such as when there is a list of products or just one
        
        try:
            if len(product):
                for object in product:
                    ratings = []
                    for comment in CandyComment.objects.filter(candy_product=object):
                        ratings.append(comment.rating)
                    if ratings:
                        object.candy_rating = mean(ratings)
                    else:
                        object.candy_rating = 0

                return product
            
        except:
            ratings = []

            for comment in CandyComment.objects.filter(candy_product=product):
                ratings.append(comment.rating)

            if ratings:
                product.candy_rating = mean(ratings)
            else:
                product.candy_rating = 0

            return product
                

class CartMixin():
    def get_cart_values(self, request):
        # Gets all the items linked to the user and assigns a variable and iterates through all the items that are linked to the user and gets the total for those items and returns a context
        
        cart = CartObject.objects.filter(linked_user=request.user).order_by("-id")
        
        subtotal = 0
        for product in cart:
            subtotal += round(product.item.cost, 2)
        subtotal = float(subtotal)

        shipping = float(0) if subtotal > 25 else round(float(subtotal) * 0.06, 2)
        sales_tax = round(float(subtotal) * 0.05, 2)

        total = round(subtotal + shipping + sales_tax, 2)

        context = {
            "cart": cart,
            "subtotal": subtotal,
            "shipping": shipping,
            "sales_tax": sales_tax,
            "total": total
        }
        return context
    
class ProfileMixin(ProductRatingMixin):
    def get_user_details(self,request, user):
        # gets all the users items and the ratings for the products and returns a context with all those calls to be used later

        preview_products = self.get_products_rating(request, Candy.objects.filter(seller = user).order_by("-id")[:3])
        all_products = self.get_products_rating(request, Candy.objects.filter(seller = user).order_by("-id"))
        comments = CandyComment.objects.filter(user=user)

        context = {
            "user" : user,
            "preview_products" : preview_products,
            "all_products" : all_products,
            "comments" : comments ,}
        return context
    