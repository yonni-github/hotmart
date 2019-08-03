from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
# import for Categories with MPTT
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    address_line = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=2, default='')
    zip_code = models.IntegerField(default=0)
    email_address = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.user.username

    def create_profile(sender, **kwargs):
        if kwargs['created']:  # If User object has been created
            # create a userprofile from the current user instance. Pass in User object to the create function
            user_profile = UserProfile.objects.create(user=kwargs['instance'])

    # connect to the post_save signal .connect(function, sender)
    post_save.connect(create_profile, sender=User)


# To handle shopping categories, using the MPTT Library
class Category(MPTTModel):
    name = models.CharField(max_length=250, default='')
    slug = models.SlugField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    category_image = models.ImageField(upload_to='category_images', default='/category_images/missing-image.png')

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


# Item model
class Item(models.Model):
    category = TreeForeignKey('Category', null=True, blank=True)
    name = models.CharField(max_length=250, default='')
    slug = models.SlugField()
    description = models.CharField(max_length=500, null=True)
    product_details = models.CharField(max_length=500, null=True)
    ingredients = models.CharField(max_length=500,null=True)
    producer = models.CharField(max_length=100,null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    item_image = models.ImageField(upload_to='item_images', default='', blank=True)

    def __str__(self):
        return self.name

    # returns the list of slugs for each Item.
    def get_slug_list_for_categories(self):
        try:
            ancestors = self.category.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]

        slugs = []

        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))

        return slugs

