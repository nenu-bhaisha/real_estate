from django.contrib import admin
from .models import admin_detail, bookmarked_property, contact_us, property, property_image, property_rented_sold, subscribe, user_details, user_review


# Register your models here.
admin.site.register(admin_detail)
admin.site.register(bookmarked_property)
admin.site.register(contact_us)
admin.site.register(property)
admin.site.register(property_image)
admin.site.register(property_rented_sold)
admin.site.register(subscribe)
admin.site.register(user_details)
admin.site.register(user_review)

