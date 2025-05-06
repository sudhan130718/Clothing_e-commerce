from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password2 = forms.CharField(
    label="Confirm Password",
    widget=forms.PasswordInput,
    help_text="Re-type your password"
)  


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,  # Hides the help text
            # 'password2': None,
        }


# Checkout

from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(max_length=255)
    apartment = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=10)
    
    # Payment details
    cardholder_name = forms.CharField(max_length=100, required=False)
    card_number = forms.CharField(max_length=16, required=False)
    expiry_date = forms.CharField(max_length=5, required=False)
    cvv = forms.CharField(max_length=3, required=False)
    
    # Payment method choice
    payment_method = forms.ChoiceField(choices=[
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
        ('card', 'Credit/Debit Card')
    ])


    def clean(self):
        cleaned_data = super().clean()
        # Optional: Add validation for card details if payment_method is 'card'
        if cleaned_data.get('payment_method') == 'card':
            card_number = cleaned_data.get('card_number')
            expiry_date = cleaned_data.get('expiry_date')
            cvv = cleaned_data.get('cvv')
            if not card_number or not expiry_date or not cvv:
                raise forms.ValidationError('Please provide all card details.')
        return cleaned_data

    address = forms.CharField(max_length=255)
    apartment = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=10)
    cardholder_name = forms.CharField(max_length=100, required=False)
    card_number = forms.CharField(max_length=16, required=False)
    expiry_date = forms.CharField(max_length=5, required=False)
    cvv = forms.CharField(max_length=3, required=False)
    payment_method = forms.ChoiceField(choices=[
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
        ('card', 'Credit/Debit Card')
    ])

