from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from .models import *

class CandyForm(ModelForm):
    class Meta:
        model = Candy
        exclude = ["seller", "candy_rating"]
        widgets = {
            "brand" : forms.TextInput(attrs={"class" : "input_field", "placeholder" : "Enter The Product's Brand . . .", "required" : "True", "autocomplete" : "off"}),
            "brand_url" : forms.URLInput(attrs={"class" : "input_field", "placeholder" : "Enter The Brand URL . . .", "required" : "False", "autocomplete" : "off"}),
            "candy_name" : forms.TextInput(attrs={"class" : "input_field", "placeholder" : "Enter The Product Name . . .", "required" : "True", "autocomplete" : "off"}),
            "candy_description" : forms.Textarea(attrs={"class" : "input_field", "placeholder" : "Enter The Product Description [Optional]", "autocomplete" : "off"}),
            "cost" : forms.TextInput(attrs={"class" : "input_field", "placeholder" : "Enter The Product's Cost . . .", "required" : "True", "autocomplete" : "off"}),
            "retail_cost" : forms.TextInput(attrs={"class" : "input_field", "placeholder" : "Enter The Product's Retail Price . . .", "required" : "True", "autocomplete" : "off"}),
            "package_weight_lbs" : forms.TextInput(attrs={"class" : "input_field", "placeholder" : "Enter The Product's Weight (lbs) . . .", "required" : "True", "autocomplete" : "off"}),
        }
        labels = {
            "brand" : "Product Brand",
            "brand_url" : "Product Brand Website",
            "candy_name" : "Product Name",
            "candy_description" : "Product Description",
            "candy_image" : "Product Photo/Image",
            "in_stock" : "Is the product currently in-stock?",
            "cost" : "Product Cost",
            "retail_cost" : "Retail Cost",
            "package_weight_lbs" : "Rounded Product Weight (to the nearest hundredth pound)."
        }
    
class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label = "Password",
        widget = forms.PasswordInput(attrs={'placeholder': 'At least 8 characters', 'class': 'input_field'})
    )
    password2 = forms.CharField(
        label = "Enter Password Again",
        widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Previous Password', 'class': 'input_field'})
    )
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Dont Include Personal Info', 'class': 'input_field', "autocomplete": "off"}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email Adress', 'class': 'input_field', 'required': True, "autocomplete": "off"}),
        }

class LoginForm(forms.Form):
    username_input = forms.CharField(max_length=100, label="Username", widget=forms.TextInput(attrs={"placeholder": "Enter Username", "class" : "input_field", "autocomplete" : "off"}))
    password_input = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter Password", "class" : "input_field"}))
    captcha = ReCaptchaField()

class CandyCommentForm(ModelForm):
    rating = forms.FloatField(
        label="Please provide a rating on a scale of 1 to 5.",
        widget=forms.NumberInput(attrs={"min": 0, "max": 5, "class" : "input_field", "placeholder" : "Rate your experience from 1-5"})
    )
    class Meta:
        model = CandyComment
        fields = ["title", "rating", "comment"]
        widgets = {
            "title" : forms.TextInput(attrs={"class" : "input_field", "placeholder" : "Enter a title name:", "required" : "True", "autocomplete" : "off"}),
            "comment" : forms.Textarea(attrs={"class" : "input_field ta_field", "placeholder" : "How was your experience?", "autocomplete" : "off"})
        }
        labels = {
            "title" : "Review Title:"
        }