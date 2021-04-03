from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import package, UserSubscription
from real_estate import settings
from django.contrib import messages
import stripe # new
stripe.api_key = settings.STRIPE_SECRET_KEY # new
import datetime
from django.utils import timezone
# Create your views here.


@login_required
def PricingTableView(request):
    if request.user.customer.Type == 'SL':
        context={}
        flag = True
        try:
            user_sub = UserSubscription.objects.get(name=request.user)
            flag = False
        except:
            flag = True
        context = {
            'package' : package.objects.all(),
            'flag' : flag,
            'key' : settings.STRIPE_PUBLISHABLE_KEY
        }
        return render(request,'payment/pricing-table.html',context)


@login_required
def CheckoutPageView(request,id_p):
    if request.user.customer.Type == 'SL':
        context= {
        'package' : package.objects.all(),
        'flag' : False,
        'key' : settings.STRIPE_PUBLISHABLE_KEY,
        }
        try:
            check_package=package.objects.get(id=id_p)
        except package.DoesNotExist:
            return redirect('pricing-table')

        try:
            sub_cust = UserSubscription.objects.get(name=request.user)
            if sub_cust.pack.id == id_p and sub_cust.sub_status == 'S':
                messages.info(request,"You have already subscribed to this plan")
                return render(request,'payment/pricing-table.html',context)
            elif sub_cust.sub_status != 'N' and check_package.package_type == 'Free':
                messages.info(request,"You can't subscribe to Free plan")
                return render(request,'payment/pricing-table.html',context)
        except:             
            price =check_package.price * 100
            checkout={
                'pack' :check_package,
                'key' : settings.STRIPE_PUBLISHABLE_KEY,
                'price' : price
            }
            return render(request,'payment/checkout.html',checkout)
        messages.info(request,"You have already subscribed to a plan")
        return render(request,'payment/pricing-table.html',context)



@login_required
def FreeSub(request,id_p):
    if request.user.customer.Type == 'SL':
        context= {'package' : package.objects.all(),'key' : settings.STRIPE_PUBLISHABLE_KEY,}
        try:
            pack=package.objects.get(id=id_p)
        except:
            print ('zahid')
            messages.info(request,"You can't subscribe to Free plan")
            return render(request,'payment/pricing-table.html',context)        

        try:
            subscriber=UserSubscription.objects.get(name_id=request.user)
            if subscriber.sub_status != 'N':
                messages.info(request,"You can't subscribe to Free plan")
                return render(request,'payment/pricing-table.html',context)  

        except UserSubscription.DoesNotExist:
            subscriber=UserSubscription.objects.create(sub_status='None',
            name=request.user) 
        subscriber.pack=package.objects.get(id=id_p)
        subscriber.paid_count=1
        subscriber.sub_status='S'
        subscriber.sub_date=timezone.now()
        subscriber.post_count = 0
        subscriber.save()


        sub_context={
            'package':pack
        }
        
        return render(request,'payment/charge.html',sub_context)



@login_required
def Charge(request,id_p):
    if request.user.customer.Type == 'SL':      
        context= {
        'package' : package.objects.all(),
        'key' : settings.STRIPE_PUBLISHABLE_KEY,
        }
        
        if request.method == 'POST':
            check_user=request.user
            try:
                pack=package.objects.get(id=id_p)
            except:
                return render(request,'payment/pricing-table.html',context)
            
            if pack.package_type == 'Free':
                return render(request,'payment/pricing-table.html',context)

            try:
                try:
                    subscriber=UserSubscription.objects.get(name_id=request.user)
                except UserSubscription.DoesNotExist:
                    subscriber=UserSubscription.objects.create(sub_status='None',
                    name=request.user) 
                if not subscriber.stripe_cust_id:
                    stripe_cust=stripe.Customer.create(
                    name=check_user.first_name,
                    email=check_user.email,
                    phone=check_user.customer.phone,
                    address={
                        'line1' :check_user.customer.country,
                        'country':check_user.customer.country,
                        'state': check_user.customer.country,
                        'city':check_user.customer.city,
                        'postal_code':check_user.customer.zip_code,
                    })
                    subscriber.stripe_cust_id=stripe_cust['id']
                else: 
                    stripe_cust=stripe.Customer.retrieve(subscriber.stripe_cust_id)
                
                            
                
                stripe_card=stripe.Customer.create_source(stripe_cust['id'], source=request.POST['stripeToken'],)
                
                charge = stripe.Charge.create(
                    amount=(pack.price)*100, # it is in docs, multiply 100 for cents 
                    currency='usd',
                    customer=stripe_cust,
                    description='Real Estate Agency charge',
                    source=stripe_card['id'],
                    metadata={'integration_check': 'accept_a_payment'},
                )
                stripe.PaymentIntent.create(
                    amount=(pack.price)*100,
                    currency="usd", 
                    payment_method=stripe_card,
                    payment_method_types=["card"],
                    confirm=True,
                    customer=stripe_cust,
                )
            except stripe.error.CardError as e:
                messages.info(request,"Your Card has been declined")
                return render(request,'payment/pricing-table.html',context)
            
            
            subscriber.pack=package.objects.get(id=id_p)
            subscriber.paid_count=1
            subscriber.sub_status='S'
            subscriber.sub_date=timezone.now()
            subscriber.post_count = 0
            subscriber.save()


            sub_context={
                'package':pack
            }
            
            return render(request,'payment/charge.html',sub_context)
        else:
        
            return render(request,'payment/pricing-table.html',context)
