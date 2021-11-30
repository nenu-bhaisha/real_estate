from smtplib import SMTPException
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, response, HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.views.generic import TemplateView
from .models import *
from .models import user_details, property, property_image, subscribe, agent_data, bookmarked_property
from django.db import connection
import os
import os.path

# Create your views here.
from django.urls import reverse
from django.conf import settings


# ============  home view ==========================
def home(request):
    if request.method == "POST":
        to_email = request.POST.get('email')
        # subscribe.objects.create(subscribe_email=to_email)

        try:
            send_mail(
                'Subscription Successfully',
                'You have subscription In.',
                settings.EMAIL_HOST_USER,
                [to_email],
                fail_silently=False)
            messages.success(request, "Your subscription successfull...")

        except SMTPException:
            return HttpResponse('SMTP Error')
        except:
            return HttpResponse('Unknown Error')
    else:

        property_details = property.objects.raw(
            'SELECT * FROM userside_property p , userside_property_rented_sold s where p.property_id<>s.property_rented_sold_property_id_id and p.property_is_publish=1;')

        p_id = property.objects.values_list('property_id')
        print('p_id', p_id)

        # photo = property_image.objects.raw('select property_image_id,property_image_url from userside_property_image where property_id_id = 18')
        photo = property_image.objects.all()

        # p_image_id = property_image.objects.raw('select property_image_id,property_id_id from userside_property_image')
        p_type = property.objects.raw(
            "select property_id,COUNT(*) from userside_property WHERE property_type = 'Apartment'")

        # Agent Data
        cursor = connection.cursor()
        cursor.execute("call AgentDataView()")
        agent = cursor.fetchall()

        data = {}
        data['property_details'] = property_details
        data['photo'] = photo
        data['p_id'] = p_id
        data['p_type'] = p_type
        city = property.objects.values('property_city').distinct()
        p_type = q = property.objects.values('property_type').distinct()
        data['city_passed'] = city
        data['property_passed'] = p_type
        data['agent_data'] = agent

        return render(request, 'user/home.html', data)
        # return render(request, 'user/home.html', {"data": data, "city_passed": city, "property_passed": p_type})


# ========= AUTHENTICATION ========
def register(request):
    if request.POST:
        rusername = request.POST['rusername']
        remail = request.POST['remail']
        rcontactno = request.POST['rcontactno']
        rpassword = request.POST['rpassword']
        rcpassword = request.POST['rcpassword']
        if user_details.objects.filter(user_email=remail).exists():
            messages.error(request, "This username already exists !!", extra_tags="warning")
            return render(request, 'user/home.html')

        elif rusername == "":
            messages.error(request, "Please Enter Full name !!", extra_tags="warning")
            return render(request, 'user/home.html')

        elif remail == "":
            messages.error(request, "Please Enter Email ID !!", extra_tags="warning")
            return render(request, 'user/home.html')

        elif rcontactno == "":
            messages.error(request, "Please Enter Contact Number !!", extra_tags="warning")
            return render(request, 'user/home.html')

        elif rpassword == "":
            messages.error(request, "Please Enter Password !!", extra_tags="warning")
            return render(request, 'user/home.html')

        elif rcpassword == "":
            messages.error(request, "Please Enter Confirm Password !!", extra_tags="warning")
            return render(request, 'user/home.html')

        elif rcpassword != rpassword:
            messages.error(request, "Password mismatch !!", extra_tags="warning")
            return render(request, 'user/home.html')


        else:
            try:
                # encrpt_password = make_password(rpassword)
                newUser = user_details.objects.create(user_name=rusername, user_email=remail, user_contact=rcontactno,
                                                      user_password=rpassword, user_image="", user_is_active=True)
                newUser.save()
                return render(request, 'user/home.html')
            except:
                return render(request, 'user/404.html')
    return render(request, 'user/home.html')


def login(request):
    if request.POST:
        print("second login block")
        login_user = request.POST['lusername']
        login_password = request.POST['lpassword']
        logged_user = None
        logged_user = user_details.objects.get(user_email=login_user, user_password=login_password)
        request.session['user_session'] = logged_user.user_id
        request.session['user_name'] = logged_user.user_name
        if logged_user is not None:
            print("third login block")
            print(f"Logged in user is {logged_user.user_id}")
            return redirect("/home")
    return render(request, 'user/home.html')


def change_password(request):
    return render(request, 'user/change-password.html')


def change_password_view(request):
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_cpassword = request.POST['new_cpassword']
        # Check Data is Avialable or not.
        user_session = request.session.get('user_session')

        try:
            if old_password == "":
                messages.error(request, "Please Enter old password !!")
                return render(request, 'user/change-password.html')
            if new_password == "":
                messages.error(request, "Please Enter new password !!")
                return render(request, 'user/change-password.html')
            if new_cpassword == "":
                messages.error(request, "Please Enter new confirm password !!")
                return render(request, 'user/change-password.html')
            elif new_cpassword != new_password:
                messages.error(request, "Password not Match !!")
                return render(request, 'user/change-password.html')
            else:
                user = user_details.objects.get(user_id=user_session, user_password=old_password)
                user.user_password = new_password
                user.save()
                messages.success(request, "Your password has been changed !!")
                return render(request, 'user/change-password.html')
        except ObjectDoesNotExist:
            messages.error(request, "Please Enter old password correctly !!")
            return render(request, 'user/change-password.html')


def logout(request):
    request.session.clear()
    return redirect('/')


# ========= PROPERTY ===========

def submit_property(request):
    if request.method == 'POST':
        property_title = request.POST.get('property_title')
        property_status = request.POST.get('status')
        property_type = request.POST.get('ptypes')
        property_price = request.POST.get('price')
        property_area = request.POST.get('area')
        property_no_of_bedrooms = request.POST.get('no_of_bedrooms')
        property_no_of_bathrooms = request.POST.get('no_of_bathrooms')
        property_address = request.POST.get('address')
        property_city = request.POST.get('city')
        property_state = request.POST.get('state')
        property_zipcode = request.POST.get('zipcode')
        property_description = request.POST.get('description')
        user = request.session.get('user_session')
        user_id = user_details.objects.get(user_id=user)
        property_added_date = datetime.today()

        # for image in property_photos:

        property_is_publish = True
        other_features = []
        if request.POST.get('a-1'):
            other_features.append('AC')
        if request.POST.get('a-2'):
            other_features.append('Bedding')
        if request.POST.get('a-3'):
            other_features.append('Heating')
        if request.POST.get('a-4'):
            other_features.append('Internet')
        if request.POST.get('a-5'):
            other_features.append('Microwave')
        if request.POST.get('a-6'):
            other_features.append('Smoking Allow')
        if request.POST.get('a-7'):
            other_features.append('Terrance')
        if request.POST.get('a-8'):
            other_features.append('Balcony')
        if request.POST.get('a-9'):
            other_features.append('Icon')
        if request.POST.get('a-10'):
            other_features.append('Wi-Fi')
        if request.POST.get('a-11'):
            other_features.append('Beach')
        if request.POST.get('a-12'):
            other_features.append('Parking')
        save_data = property.objects.create(property_title=property_title, property_status=property_status,
                                            property_type=property_type, property_price=property_price,
                                            property_sqft_area=property_area, property_bedrooms=property_no_of_bedrooms,
                                            property_bathrooms=property_no_of_bathrooms,
                                            property_address=property_address,
                                            property_city=property_city, property_state=property_state,
                                            property_zipcode=property_zipcode,
                                            property_description=property_description,
                                            property_user_id=user_id, property_added_date=property_added_date,
                                            property_others=other_features, property_is_publish=property_is_publish)
        save_data.save()
        # Code for uploading Multiple Image
        property_photos = request.FILES.getlist('property_photos')
        for img in property_photos:
            property_image.objects.create(property_image_url=img, property_id=save_data)
        messages.error(request, "Property Save Successfully !!", extra_tags="success")
    return render(request, 'user/submit-property.html')


def single_property(request, p_id):
    property_details = property.objects.get(property_id=p_id)
    review = user_review.objects.filter(user_review_property_id=p_id)
    rcount = user_review.objects.filter(user_review_property_id=p_id).count()

    p_others = property.objects.raw(
        '''select property_id,property_others from userside_property where property_id = %s''', [p_id])

    for p in p_others:
        print(p.property_others)
    l_time = range(len(p_others))

    property_photo = property_image.objects.raw(
        'select property_image_id,property_image_url from userside_property_image where property_id_id = %s', [p_id])
    for p in property_photo:
        print(p.property_image_url)

    data = {}
    data['property_details'] = property_details
    data['property_photo'] = property_photo
    data['p_others'] = p_others
    data['l_time'] = l_time
    data['review'] = review
    data['rcount'] = rcount

    return render(request, 'user/single-property.html', data)


def user_reviews(request, property_id):
    if request.method == 'POST':
        if request.session.get('user_session'):
            rmessage = request.POST.get('rmessage')
            user_session = request.session.get('user_session')

            user_review.objects.create(
                user_review_message=rmessage,
                user_review_property_id=property.objects.get(property_id=property_id),
                user_review_user_id=user_details.objects.get(user_id=user_session)
            )
            return redirect("/home")
            # return render(request, 'user/single-property.html', {"p_id": property_id})
    return redirect("/home")


def property_type(request):
    if request.method == 'POST':
        city_selected = request.POST.get('property_city_option')
        property_type_selected = request.POST.get('property_type_option')
        photo = property_image.objects.all()
        print(f"city is {city_selected} and property type is {property_type_selected}")
        # pselected = property.objects.values_list('property_id', flat=True).filter(property_type=property_type_selected, property_city=city_selected)
        pselected = property.objects.filter(property_type=property_type_selected, property_city=city_selected)
        # p = property.objects.filter(property_id=i)
        print(f"selected city is ->>>>{city_selected}  and {property_type_selected}")
        print(f"selected property is ->>>>{pselected}")
    return render(request, 'user/property_type.html', {"pselected": pselected, "photo": photo})


def property_type1(request, property_status):
    pselected = property.objects.filter(property_status=property_status)
    photo = property_image.objects.all()
    print(f"Pseleceted {pselected} and {photo}--------")
    # return ('/property_type', {"pselected": pselected, "photo": photo})
    return render(request, 'user/property_type.html', {"pselected": pselected, "photo": photo})

def property_type2(request, property_type):
    pselected = property.objects.filter(property_type=property_type)
    photo = property_image.objects.all()
    print(f"Pseleceted {pselected} and {photo}--------")
    # return ('/property_type', {"pselected": pselected, "photo": photo})
    return render(request, 'user/property_type.html', {"pselected": pselected, "photo": photo})

def property_type_filter(request):
    if request.method == 'POST':
        ptype = request.POST.get('ptype')
        status = request.POST.get('status')
        price = request.POST.get('price')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        min_area = request.POST.get('min_area')
        max_area = request.POST.get('max_area')
        photo = property_image.objects.all()

        if price == 1:
            pselected = property.objects.filter(property_type=ptype, property_status=status,
                                                property_price__range=(0, 10000), property_bedrooms=bedrooms,
                                                property_bathrooms=bathrooms,
                                                property_sqft_area__range=(min_area, max_area))
        elif price == 2:
            pselected = property.objects.filter(property_type=ptype, property_status=status,
                                                property_price__range=(10000, 100000), property_bedrooms=bedrooms,
                                                property_bathrooms=bathrooms,
                                                property_sqft_area__range=(min_area, max_area))
        elif price == 3:
            pselected = property.objects.filter(property_type=ptype, property_status=status,
                                                property_price__range=(100000, 500000), property_bedrooms=bedrooms,
                                                property_bathrooms=bathrooms,
                                                property_sqft_area__range=(min_area, max_area))
        elif price == 4:
            pselected = property.objects.filter(property_type=ptype, property_status=status,
                                                property_price__range=(500000, 5000000), property_bedrooms=bedrooms,
                                                property_bathrooms=bathrooms,
                                                property_sqft_area__range=(min_area, max_area))
        else:
            pselected = property.objects.filter(property_type=ptype, property_status=status,
                                                property_price__range=(5000000, 50000000000),
                                                property_bedrooms=bedrooms,
                                                property_bathrooms=bathrooms,
                                                property_sqft_area__range=(min_area, max_area))

        print(f"========================================selected property is ->>>>{pselected}")
    return render(request, 'user/property_type.html', {"pselected": pselected, "photo": photo})
    # return render(request, '/user/property_type.html', {"pselected": pselected, "photo": photo})


# ========= AGENT ===========

def agent(request):
    cursor = connection.cursor()
    # AgenyDataView() is Procedure Name. it is create in phpMyAdmin
    cursor.execute("call AgentDataView()")
    agent = cursor.fetchall()
    # agent = property.objects.raw('''SELECT p.property_id, p.property_user_id_id, count(p.property_id) as c, u.user_id, u.user_name, u.user_email, u.user_contact, u.user_image, u.user_city, u.user_state, u.user_facebook, u.user_instagram, u.user_linkedin, u.user_twitter FROM `userside_user_details` u, `userside_property` p where u.user_id = p.property_user_id_id group by p.property_user_id_id''')
    return render(request, 'user/agents.html', {"agent_data": agent})


def agent_details(request, id):
    agent_detail = user_details.objects.get(user_id=id)
    property_details = property.objects.raw(
        'SELECT * FROM userside_property p , userside_property_rented_sold s where p.property_id<>s.property_rented_sold_property_id_id and p.property_is_publish=1;')
    photo = property_image.objects.all()
    return render(request, 'user/agent-page.html', {"agent": agent_detail,"property_details":property_details,"photo":photo})


# ========== USER ===========
class ClubChartView(TemplateView):
    template_name = 'user/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = property.objects.all()
        return context
        # return render(request, 'user/chart.html')


def user_dashboard(request):
    user_session = request.session.get('user_session')
    labels = []
    data = []

    pbcount = bookmarked_property.objects.filter(bookmarked_property_user_id_id=user_session).count()
    user = user_details.objects.get(user_id=user_session) 
    
    queryset = property.objects.order_by('-property_id')
    for city in queryset:
        labels.append(property.property_added_date)
        data.append(property.property_is_publish)

    return render(request, 'user/user_dashboard.html', {
        'labels': labels,
        'data': data,
        "user":user,
        "pbcount":pbcount
    })


def user_profile(request):
    user_session = request.session.get('user_session')
    pbcount = bookmarked_property.objects.filter(bookmarked_property_user_id_id=user_session).count()

    if request.method == "POST":
        uname = request.POST['uname']
        uemail = request.POST['uemail']
        utitle = request.POST['utitle']
        ucontact = request.POST['ucontact']
        uaddress = request.POST['uaddress']
        ucity = request.POST['ucity']
        ustate = request.POST['ustate']
        uzipcode = request.POST['uzipcode']
        uabout = request.POST['uabout']
        ufacebook = request.POST['ufacebook']
        utwitter = request.POST['utwitter']
        uinstagram = request.POST['uinstagram']
        ulinkedin = request.POST['ulinkedin']
                
        if uname == "":
            messages.error(request, "Please Enter Full name !!")
            return render(request, 'user/user_profile.html')
        if uemail == "":
            messages.error(request, "Please Enter EmailID !!")
            return render(request, 'user/user_profile.html')
        if ucontact == "":
            messages.error(request, "Please Enter Contact Number !!")
            return render(request, 'user/user_profile.html')
        else:
            user = user_details.objects.get(user_id=user_session)
            user.user_name = uname
            user.user_email = uemail
            user.user_title = utitle
            user.user_contact = ucontact
            user.user_address = uaddress
            user.user_city = ucity
            user.user_state = ustate
            user.user_zipcode = uzipcode
            user.user_about = uabout
            user.user_facebook = ufacebook
            user.user_twitter = utwitter
            user.user_instagram = uinstagram
            user.user_linkedin = ulinkedin
            
            if len(request.FILES) != 0:
                # if len(user.user_image) > 0:
                    # os.remove(user.user_image.path)
                user.user_image = request.FILES.get('change_image')

            user.save()
            messages.success(request, "Your Profile has been updated !!")
            return render(request, "user/user_profile.html", {"user": user})

    else:
        user = user_details.objects.get(user_id=user_session)
        return render(request, "user/user_profile.html", {"user": user,"pbcount":pbcount})

    return render(request, 'user/user_profile.html')


def user_property(request):
    user_session = request.session.get('user_session')
    property_info = property.objects.filter(property_user_id=user_session)
    photo = property_image.objects.all()
    property_sold = property_rented_sold.objects.all()
    
    pbcount = bookmarked_property.objects.filter(bookmarked_property_user_id_id=user_session).count()
    user = user_details.objects.get(user_id=user_session)    

    
    return render(request, 'user/user_property.html',
                  {"property_info": property_info, "property_sold": property_sold, "photo": photo,"user":user,"pbcount":pbcount})


def edit_property(request, property_id):
    property1 = property.objects.get(property_id=property_id)
    return render(request, "user/edit_property.html", {"property1": property1})


def edit_property_view(request):
    if request.method == "POST":
        property_id = request.POST.get('property_id')
        property_title = request.POST.get('property_title')
        property_status = request.POST.get('status')
        property_type = request.POST.get('ptypes')
        property_price = request.POST.get('price')
        property_area = request.POST.get('area')
        property_no_of_bedrooms = request.POST.get('no_of_bedrooms')
        property_no_of_bathrooms = request.POST.get('no_of_bathrooms')
        property_address = request.POST.get('address')
        property_city = request.POST.get('city')
        property_state = request.POST.get('state')
        property_zipcode = request.POST.get('zipcode')
        property_description = request.POST.get('description')
        property_is_publish = request.POST.get('publish')

        user_session = request.session.get('user_session')

        try:
            if property_title == "":
                messages.error(request, "Please Enter property title !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_status == "":
                messages.error(request, "Please Enter property status !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_type == "":
                messages.error(request, "Please Enter property type !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_price == "":
                messages.error(request, "Please Enter property price !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_area == "":
                messages.error(request, "Please Enter property area !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_no_of_bedrooms == "":
                messages.error(request, "Please Enter number of bedrooms in property !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_no_of_bathrooms == "":
                messages.error(request, "Please Enter number of bathrooms in property !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_address == "":
                messages.error(request, "Please Enter property address !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_city == "":
                messages.error(request, "Please Enter property city !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_state == "":
                messages.error(request, "Please Enter property state !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_zipcode == "":
                messages.error(request, "Please Enter property zipcode !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')
            elif property_description == "":
                messages.error(request, "Please Enter property area description !!", extra_tags="warning")
                return render(request, 'user/edit_property.html')

            else:
                property1 = property.objects.get(property_id=property_id)
                property1.property_id = property_id
                property1.property_title = property_title
                property1.property_status = property_status
                property1.property_type = property_type
                property1.property_price = property_price
                property1.property_sqft_area = property_area
                property1.property_bedrooms = property_no_of_bedrooms
                property1.property_bathrooms = property_no_of_bathrooms
                property1.property_address = property_address
                property1.property_city = property_city
                property1.property_state = property_state
                property1.property_zipcode = property_zipcode
                property1.property_description = property_description
                property1.property_is_publish = property_is_publish
                property1.save()
                messages.success(request, "Your property has been updateded !!")
                return redirect("user-property")
        except ObjectDoesNotExist:
            messages.error(request, "Please Enter old password correctly !!")
            return redirect("user-property")


def view_property(request, property_id):
    property1 = property.objects.get(property_id=property_id)
    property_photo = property_image.objects.filter(property_id=property_id)
    return render(request, "user/view_property.html", {"property1": property1, "property_photo": property_photo})


def delete_property(request, property_id):
    property1 = property.objects.get(property_id=property_id)
    property1.property_is_publish = False
    property1.save()
    return redirect("user-property")


def user_bookmark_list(request):
    user_session = request.session.get('user_session')
    bookmark = bookmarked_property.objects.filter(bookmarked_property_user_id=user_session)
    property_info = property.objects.all()
    photo = property_image.objects.all()

    pbcount = bookmarked_property.objects.filter(bookmarked_property_user_id_id=user_session).count()
    user = user_details.objects.get(user_id=user_session)    

    return render(request, 'user/user_bookmark-list.html',
                  {"property_info": property_info, "bookmark": bookmark, "photo": photo,"user":user,"pbcount":pbcount})

def add_bookmark(request, property_id):
    user_session = request.session.get('user_session')
    add = bookmarked_property.objects.filter(
        bookmarked_property_property_id=property.objects.get(property_id=property_id),
        bookmarked_property_user_id=user_details.objects.get(user_id=user_session))

    if not add:
        bookmarked_property.objects.create(
            bookmarked_property_property_id=property.objects.get(property_id=property_id),
            bookmarked_property_user_id=user_details.objects.get(user_id=user_session)
        )
        messages.success(request, "Bookmarked Successfully !!")
    else:
        messages.warning(request, "Already Bookmarked !!")

    return redirect("user-bookmark_list")
    # return render(request, 'user/user_bookmark-list.html')

def delete_bookmark(request, property_id):
    user_session = request.session.get('user_session')
    bookmark = bookmarked_property.objects.filter(bookmarked_property_user_id=user_session,
                                                  bookmarked_property_property_id=property_id)
    bookmark.delete()
    messages.success(request, "Bookmarked Removed !!")
    return redirect("user-bookmark_list")

# ====== OTHERS ====================

def about(request):
    return render(request, 'user/about.html')


def contact(request):
    if request.method == "POST":

        # ---------------Save Data In Database-------------------

        contact_Name = request.POST.get('contact_Name')
        contact_Email = request.POST.get('contact_Email')
        contact_Subject = request.POST.get('contact_Subject')
        contact_Message = request.POST.get('contact_Message')
        print("Coneatasdfasdfasd", contact_Email)
        contact_us.objects.create(contact_name=contact_Name, contact_email=contact_Email, contact_contact=0,
                                  contact_subject=contact_Subject, contact_message=contact_Message)

        # --------------------Send mail to via Email --------------

        try:
            send_mail(
                contact_Subject,
                contact_Message,
                contact_Email,
                ['rentup.help@gmail.com'],
                fail_silently=False)
            messages.success(request, "We are contact you !")
        except SMTPException:
            return HttpResponse('SMTP Error')
        except:
            return HttpResponse('Unknown Error')

        return render(request, 'user/contact.html')
    else:
        return render(request, 'user/contact.html')


def faq(request):
    return render(request, 'user/faq.html')


def privacy(request):
    return render(request, 'user/privacy.html')


def not_found_404(request):
    return render(request, 'user/404.html')


def subscribe(request):
    if request.POST:
        semail = request.POST['semail']
        if subscribe.objects.filter(subscribe_email=semail).exists():
            return render(request, 'user/home.html')

        else:
            try:
                # encrpt_password = make_password(rpassword)
                newSubscribe = subscribe.objects.create(subscribe_email=semail)
                newSubscribe.save()
                return render(request, 'user/home.html')
            except:
                return HttpResponse("404")

    return render(request, 'user/home.html')
