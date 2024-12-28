from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'), unique=True)
    password = models.CharField(_('Password'), max_length=128)
    phone_number = models.CharField(_('Phone Number'), max_length=15, blank=True, null=True)
    address = models.TextField(_('Address'), blank=True, null=True)
    registration_date = models.DateTimeField(_('Registration Date'), auto_now_add=True)

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.name


class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='categories')


    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=50)
    image_url = models.ImageField(_('image url'), upload_to='products/')
    description = models.TextField(_('description'), blank=True)
    categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True)
    stock = models.IntegerField()
    # category_id = models.ForeignKey(to_field=Category)
    price = models.FloatField()

    class Meta:
        db_table = 'products'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name

    class Order(models.Model):
        user = models.ForeignKey('User', verbose_name=_('User'), on_delete=models.CASCADE, related_name='orders')
        order_date = models.DateTimeField(_('Order Date'), auto_now_add=True)
        status = models.CharField(_('Status'), max_length=50,
                                  choices=[('Pending', _('Pending')), ('Completed', _('Completed')),
                                           ('Canceled', _('Canceled'))])
        total_amount = models.DecimalField(_('Total Amount'), max_digits=10, decimal_places=2)

        class Meta:
            db_table = 'orders'
            verbose_name = _('order')
            verbose_name_plural = _('orders')

        def __str__(self):
            return f"Order {self.id} by {self.user.name}"

    class Cart(models.Model):
        user = models.OneToOneField('User', verbose_name=_('User'), on_delete=models.CASCADE, related_name='cart')

        class Meta:
            db_table = 'carts'
            verbose_name = _('cart')
            verbose_name_plural = _('carts')

        def __str__(self):
            return f"Cart of {self.user.name}"

    class CartItem(models.Model):
        cart = models.ForeignKey('Cart', verbose_name=_('Cart'), on_delete=models.CASCADE, related_name='items')
        product = models.ForeignKey('Product', verbose_name=_('Product'), on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField(_('Quantity'))

        class Meta:
            db_table = 'cart_items'
            verbose_name = _('cart item')
            verbose_name_plural = _('cart items')

        def __str__(self):
            return f"{self.quantity} x {self.product.name}"

