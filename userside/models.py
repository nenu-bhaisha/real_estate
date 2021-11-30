from django.db import models

# Create your models here.
from django.db.models import ForeignKey
from sqlparse.sql import For


# admin_detail
class admin_detail(models.Model):
    admin_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL
    admin_name = models.CharField(max_length=200)  # varchar(50) NOT NULL
    admin_email = models.CharField(max_length=200)  # varchar(50) NOT NULL
    admin_contact = models.IntegerField()  # int(10) NOT NULL
    admin_image = models.CharField(max_length=200)  # varchar(100) NOT NULL
    admin_password = models.CharField(max_length=200)  # varchar(50) NOT NULL


# user_details
class user_details(models.Model):
    user_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL
    user_name = models.CharField(max_length=200)  # varchar(50) NOT NULL
    user_email = models.CharField(max_length=200)  # varchar(50) NOT NULL
    user_contact = models.IntegerField()  # int(10) NOT NULL
    user_image = models.ImageField(upload_to='User_Profile_Image',null=True)  # varchar(100) NOT NULL
    user_password = models.CharField(max_length=200)  # varchar(50) NOT NULL
    user_is_active = models.BooleanField(default=False)  # tinyint(1) NOT NULL
    user_title = models.CharField(max_length=200, null=True)
    user_address = models.CharField(max_length=500, null=True)
    user_city = models.CharField(max_length=200, null=True)
    user_state = models.CharField(max_length=200, null=True)
    user_zipcode = models.IntegerField(null=True)
    user_about = models.CharField(max_length=5000, null=True)
    user_facebook = models.CharField(max_length=200, null=True)
    user_twitter = models.CharField(max_length=200, null=True)
    user_instagram = models.CharField(max_length=200, null=True)
    user_linkedin = models.CharField(max_length=200, null=True)


    def __str__(self):
        return self.user_name


# property
class property(models.Model):
    property_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL
    property_title = models.CharField(max_length=500)  # varchar(255) NOT NULL
    property_status = models.CharField(max_length=200)  # varchar(50) NOT NULL
    property_type = models.CharField(max_length=200)  # varchar(50) NOT NULL
    # property_is_for_sell = #tinyint(1) DEFAULT NULL
    # property_is_for_rent = #tinyint(1) DEFAULT NULL
    property_price = models.IntegerField()  # int(15) DEFAULT NULL
    # property_rent = #int(15) DEFAULT NULL
    property_sqft_area = models.IntegerField()  # int(10) NOT NULL
    property_bedrooms = models.IntegerField()  # int(11) NOT NULL
    property_bathrooms = models.IntegerField()  # int(11) NOT NULL
    property_address = models.CharField(max_length=500)  # varchar(500) NOT NULL
    property_city = models.CharField(max_length=200)  # varchar(50) NOT NULL
    property_state = models.CharField(max_length=200)  # varchar(50) NOT NULL
    property_zipcode = models.IntegerField()  # int(11) NOT NULL
    property_description = models.CharField(max_length=10000)  # varchar(5000) NOT NULL
    property_others = models.CharField(max_length=500, null=True)  # varchar(5000) NOT NULL
    property_user_id = ForeignKey(user_details, on_delete=models.CASCADE)  # varchar(10) NOT NULL
    property_added_date = models.DateField()  # date NOT NULL DEFAULT current_timestamp()
    property_is_publish = models.BooleanField(null=True)  # tinyint(1) NOT NULL
    #property_photos_id = ForeignKey(property_image, on_delete=models.CASCADE)  # varchar(10) NOT NULL


    def __str__(self):
        return "{}-{}".format(self.property_id,self.property_price)

# bookmarked_property
class bookmarked_property(models.Model):
    bookmarked_property_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL
    bookmarked_property_user_id = ForeignKey(user_details, on_delete=models.CASCADE)  # varchar(10) NOT NULL
    bookmarked_property_property_id = ForeignKey(property, on_delete=models.CASCADE)  # varchar(10) NOT NULL


# contact_us
class contact_us(models.Model):
    contact_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL
    contact_name = models.CharField(max_length=200)  # varchar(100) NOT NULL
    contact_email = models.CharField(max_length=200)  # varchar(100) NOT NULL
    contact_contact = models.IntegerField()  # int(10) NOT NULL
    contact_subject = models.CharField(max_length=500)  # varchar(100) NOT NULL
    contact_message = models.CharField(max_length=10000)  # varchar(10000) NOT NULL


# property_image table
class property_image(models.Model):
    property_image_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL,
    property_id = ForeignKey(property, on_delete=models.CASCADE)  # varchar(10) NOT NULL,
    property_image_url = models.ImageField(upload_to='Property_Image',null=True)  # varchar(100) NOT NULL


# property_rented_sold
class property_rented_sold(models.Model):
    property_rented_sold_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL
    property_rented_sold_property_id = ForeignKey(property, on_delete=models.CASCADE)  # varchar(10) NOT NULL
    property_rented_sold_user_id = ForeignKey(user_details, on_delete=models.CASCADE)  # varchar(10) NOT NULL
    property_rented_sold_date = models.DateField()  # date NOT NULL DEFAULT current_timestamp()
    property_rented_sold_duration = models.IntegerField(
        null=True)  # int(11) DEFAULT NULL COMMENT '(only for rent - in months )'


# subscribe
class subscribe(models.Model):
    subscribe_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL
    subscribe_email = models.CharField(max_length=200)  # varchar(100) NOT NULL


# user_details
class user_review(models.Model):
    user_review_id = models.AutoField(primary_key=True)  # varchar(10) NOT NULL,
    user_review_user_id = ForeignKey(user_details, on_delete=models.CASCADE)  # varchar(10) NOT NULL,
    user_review_property_id = ForeignKey(property, on_delete=models.CASCADE)  # varchar(10) NOT NULL,
    user_review_message = models.CharField(max_length=2000)  # varchar(500) NOT NULL


#Procedure for agent data

class agent_data(models.Model):
    p_count = models.IntegerField()
    user_id = models.CharField(max_length=10)           #0
    user_name = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200) #1
    user_email = models.CharField(max_length=200)       #2
    user_contact = models.IntegerField()                #3
    user_image = models.CharField(max_length=200)       #4
    user_city = models.CharField(max_length=200)        #5
    user_state = models.CharField(max_length=200)       #6
    user_facebook = models.CharField(max_length=200)    #7
    user_twitter = models.CharField(max_length=200)     #8
    user_instagram = models.CharField(max_length=200)   #9
    user_linkedin = models.CharField(max_length=200)    #10