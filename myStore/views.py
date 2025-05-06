from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Category, Order, OrderItem,Product,Brand,ProductVariant,Cart, CartItem, Wishlist

from django.core.paginator import Paginator
from django.db.models import Q

from .forms import SignupForm,CheckoutForm



# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login') 
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')







def home(request):
     categories = Category.objects.filter(parent__isnull=True).order_by('position')
     return render(request, 'home.html', {'categories': categories})



def category_page(request):
    categories = Category.objects.filter(parent__isnull=True).order_by('position')
    return render(request, 'category.html', {'categories': categories})


def all_products(request):
    categories = Category.objects.filter(parent__isnull=True).order_by('position')
    products = Product.objects.prefetch_related('variants').all()

    


 


     # Get filters from query params
    selected_gender = request.GET.getlist('gender')
    selected_brand = request.GET.getlist('brand')
    selected_size = request.GET.getlist('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
       
 # Get all brands and sizes
    brands = Brand.objects.all()
    sizes = ProductVariant.objects.values_list('size', flat=True).distinct()

    search_query = request.GET.get('searchProduct', '').strip()
    print("search_query:", search_query)

    if search_query:
     products = products.filter(name__icontains=search_query)
     for p in products:
      print(p.name)
      print("products:", products)

    if selected_gender:
     products = products.filter(category__slug__in=selected_gender)

    if selected_brand:
        products = products.filter(brand__name__in=selected_brand)

    if selected_size:
        products = products.filter(variants__size__in=selected_size).distinct()

    if min_price and max_price:
        products = products.filter(variants__price__gte=min_price, variants__price__lte=max_price).distinct()


    return render(request, 'all_products.html', {
        'categories': categories,
        'products': products,
         'brands': brands,
        'sizes': sizes,
        'selected_gender':selected_gender,
        'selected_brand': selected_brand,
        'selected_size': selected_size,
    })


def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.subcategories.all()
    category_ids = [category.id] + [sub.id for sub in subcategories]
    categories = Category.objects.filter(parent__isnull=True).order_by('position')

    # Get filters from query params
    selected_brand = request.GET.getlist('brand')
    selected_size = request.GET.getlist('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(category_id__in=category_ids)

    if selected_brand:
        products = products.filter(brand__name__in=selected_brand)

    if selected_size:
        products = products.filter(variants__size__in=selected_size).distinct()

    if min_price and max_price:
        products = products.filter(variants__price__gte=min_price, variants__price__lte=max_price).distinct()

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all brands and sizes
    brands = Brand.objects.all()
    sizes = ProductVariant.objects.values_list('size', flat=True).distinct()

    return render(request, 'products.html', {
        'category': category,
        'categories': categories,
        'brands': brands,
        'sizes': sizes,
        'subcategories': subcategories,
        'page_obj': page_obj,
        'selected_brand': selected_brand,
        'selected_size': selected_size,
    })


def product_detail(request, category_slug,  product_slug):

    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.filter(parent__isnull=True).order_by('position')


    
    product = get_object_or_404(Product, slug=product_slug, )
    variant = product.variants.first()
    selected_size = variant.size if variant else None

    sizes = [size[0] for size in ProductVariant.SIZE_CHOICES]
    context = {
        'category': category,
        'categories': categories,
        'product': product,
        'sizes': sizes,
        'selected_size': selected_size,
    }
    return render(request, 'product_view.html', context)



# Cart start

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        item.quantity += 1
    item.save()
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    categories = Category.objects.filter(parent__isnull=True).order_by('position')

    return render(request, 'cart.html', {'cart': cart, 'items': items,'categories': categories})


@login_required
def update_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1

    item.save()
    return redirect('view_cart')


@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('view_cart')

# Cart end


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        categories = Category.objects.filter(parent__isnull=True).order_by('position')

        items = cart.cartitem_set.all()

        if not items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('home')

        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=form.cleaned_data['address'],
                    total_amount=cart.total(),
                    status='pending',
                    payment_method=form.cleaned_data['payment_method'],
                )

                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product_variant=item.product.variants.first(),  # ensure it's a variant
                        quantity=item.quantity,
                        price=item.product.variants.first().price,  # use variant price
                    )

                cart.cartitem_set.all().delete()
                messages.success(request, "Your order has been placed successfully!")
                return redirect('order_confirmation', order_id=order.id)
        else:
            form = CheckoutForm()

        total = cart.total()

        return render(request, 'checkout.html', {
            'form': form,
            'cart': cart,
            'items': items,
            'total': total,
            'categories': categories
        })

    except Cart.DoesNotExist:
        messages.error(request, "You don't have a cart yet.")
        return redirect('home')

@login_required
def order_confirmation(request, order_id):
    # Get the order based on the order_id
    order = get_object_or_404(Order, id=order_id)

    # Fetch the order items related to this order
    order_items = order.items.all()

    # Render the confirmation page
    return render(request, 'order_confirmation.html', {
        'order': order,
        'order_items': order_items
    })


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER', 'all_products'))  # Redirect to previous page

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect(request.META.get('HTTP_REFERER', 'all_products'))

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
