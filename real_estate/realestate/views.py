from django.shortcuts import render, redirect
from .forms import PostCreateForm, UpdatePostForm, UpdatePostMediaForm, SearchForm
from .models import post, media ,reports, suggestions
from payment.models import UserSubscription
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
from django.db.models import Q

import cv2 as cv

def home(request):
    p = post.objects.all().order_by('-id')[:3]
    medi = []
    for pt in p:
        medi.append(media.objects.filter(pst=pt))
    lastest_p = post.objects.all().order_by('-id')[:3]
    latest_medi = []
    for pt in lastest_p:
        latest_medi.append(media.objects.filter(pst=pt))    
    context = {
        'ads' : p,
        'medi' : medi,
        'Lastestads' : lastest_p,
        'latestmedi' : latest_medi,
    }
    return render(request,'realestate/home.html',context)


def contact(request):
    return render(request,'realestate/contact.html')

def about(request):
    return render(request,'realestate/about.html')


@login_required
def CreatePostView(request):
    if request.user.customer.Type == 'SL':
        try:
            sub_cust = UserSubscription.objects.get(name=request.user)
        except UserSubscription.DoesNotExist:
            messages.info(request,"You have not subscribed to any plan")
            return redirect('pricing-table')
        if sub_cust.post_count < sub_cust.pack.ad_posting_limit and (30 - (sub_cust.sub_date - datetime.date.today()).days) >= 1  :

            if request.method == 'POST':
                sub_cust.post_count += 1
                form = PostCreateForm(request.POST,request.FILES)
                if form.is_valid():
                    p=post.objects.create(author = request.user,status=form.cleaned_data['status'], location=form.cleaned_data['location'],
                                        property_type=form.cleaned_data['property_type'], area=form.cleaned_data['area'],
                                        beds=form.cleaned_data['beds'], baths=form.cleaned_data['baths'],property_desc=form.cleaned_data['property_desc'],
                                        garage=form.cleaned_data['garage'], price=form.cleaned_data['price'],)
                    files = request.FILES.getlist('image_field')            
                    for f in files:
                        media.objects.create(img=f,pst=p)
                    return redirect('my-ads')
            else:
                form = PostCreateForm()
            return render(request, 'realestate/post_form.html', {'form': form})   
        else:
            sub_cust.sub_status = 'E'
            context= {'package' : package.objects.all(),'key' : settings.STRIPE_PUBLISHABLE_KEY,}
            messages.info(request,"Your package is expire or you have reached the job posting limit")
            return render(request,'payment/pricing-tables.html',context)            


@login_required
def MyAds(request):
    if request.user.customer.Type == 'SL':
        p = post.objects.filter(author=request.user)
        medi = []
        for pt in p:
            m = media.objects.filter(pst=pt)
            medi.append(m)
        context = {
            'ads' : p,
            'medi' : medi,
        }
        # print ( p[0].area )
        return render(request, 'realestate/my_ads.html', context) 


@login_required
def UpdatePostView(request,id_p):
    p=post.objects.get(id=id_p)
    if request.user.customer.Type == 'SL' and p.author == request.user:
        if request.method == 'POST':
            form_P = UpdatePostForm(request.POST, instance=post.objects.get(id=id_p))
            form_M = UpdatePostMediaForm(request.POST,request.FILES)

                    
            if form_P.is_valid() and form_M.is_valid():
                form_P.save()
                files = request.FILES.getlist('image_field')   
                x=0
                for f in files:
                    if x==0:
                        media.objects.filter(pst=p).delete()
                    media.objects.create(img=f,pst=p)   
                    x += 1             

                return redirect('my-ads')

        else:
            form_P = UpdatePostForm(instance=post.objects.get(id=id_p))
            form_M = UpdatePostMediaForm()

        context = {
            'form_P': form_P,
            'form_M': form_M,
        }

        return render(request, 'realestate/post_update.html', context)




@login_required
def DeletePostView(request,id_p):
    p=post.objects.get(id=id_p)
    if request.user.customer.Type == 'SL' and p.author == request.user:
        if request.method == 'POST':
            post.objects.get(id=id_p).delete()
            return redirect('my-ads')
    return render(request,'realestate/post_delete.html')


@login_required
def DetailPostView(request,id_p):
    p = post.objects.get(id=id_p)

    # adding views
    found = False
    try:
        report = reports.objects.get(pst_id=id_p)
        for already_seen_by in report.seenby:
            if request.user == already_seen_by:
                found = True
                break
    except:
        report = reports.objects.create(views=0,pst=p)
    if found == False:
        report.views += 1
        report.seenby.add(request.user)
        report.save

    #adding suggestions
    found = False
    try:
        sugg = suggestions.objects.all()
        for s in sugg:
            if request.user == s.user:
                found = True
                break
        if found:
            sugg = suggestions.objects.get(user=request.user)
        else:
            sugg = suggestions.objects.create(user=request.user)
    except:
        sugg = suggestions.objects.create(user=request.user)

    if p.property_type == 'House':
        sugg.houses += 1
    else:
        sugg.plots += 1

    #print (sugg.houses,'\n\n\n')
    sugg.save()
    context = {
        'ad' : p,
        'image' : media.objects.filter(pst_id=id_p),
        'owner' : User.objects.get(id=p.author.id),
        'view' : report.views
    }  
    return render(request,'realestate/post_view.html', context)





def AllPropertiesView(request):
    p = post.objects.all()
    medi = []
    for pt in p:
        m = media.objects.filter(pst=pt)
        medi.append(m)
    try:
        sugg_p = suggestions.objects.get(user=request.user)
        if sugg_p.plots > sugg_p.houses:
            sugg = post.objects.filter(property_type='Plot')
        else:
            sugg = post.objects.filter(property_type='House')
        sugg_medi = []
        for pt in sugg:
            m = media.objects.filter(pst=pt)
            sugg_medi.append(m)
        context = {
            'ads' : p,
            'medi' : medi,
            'sugg_add' : sugg,
            'sugg_medi' : sugg_medi,
            'Sugg' : True
        }
    except:
        context = {
            'ads' : p,
            'medi' : medi,
            'Sugg' : False
        }        
    return render(request, 'realestate/view_all_properties.html', context) 










def SearchView(request):
    if request.method == 'POST':
        form_P = SearchForm(request.POST)
        
        if form_P.is_valid():
            # try:
                print (form_P)
                if form_P.cleaned_data['property_type'] == 'Plot':
                    q = post.objects.filter(Q(property_type='Plot') & Q(status=form_P.cleaned_data['status'])
                                            & Q(location=form_P.cleaned_data['city']) & Q(price__lte= form_P.cleaned_data['price']))
                else:
                    q = post.objects.filter(Q(property_type='House') & Q(status=form_P.cleaned_data['status'])
                                            & Q(location=form_P.cleaned_data['city']) & Q(price__lte=form_P.cleaned_data['price'])
                                            & Q(baths=form_P.cleaned_data['baths']) & Q(beds= form_P.cleaned_data['beds']) & Q(garage= form_P.cleaned_data['garage']))
                                            
                p = q
                medi = []
                for pt in p:
                    m = media.objects.filter(pst=pt)
                    medi.append(m)
                context = {
                    'ads' : p,
                    'medi' : medi,
                }
                return render(request, 'realestate/view_all_properties.html', context)
            # except:
            #     messages.info(request,"No Search results found")


    else:
        form_P = SearchForm()
    context = {
        'cities' : post.objects.values('location').distinct(),
        'Num_of_baths' : post.objects.values('baths').distinct(),
        'Num_of_beds' : post.objects.values('beds').distinct(),
        'Num_of_garage' : post.objects.values('garage').distinct(),
        'form_P': form_P
    }
    return render(request, 'realestate/search.html', context)



