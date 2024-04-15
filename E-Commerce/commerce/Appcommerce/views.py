import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.core.paginator import Paginator
from .signals import *
from django.contrib.auth.decorators import login_required
import iyzipay
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
import hashlib
import base64
import requests
import urllib.parse
def ProductQuantity(request):
    if request.user.is_authenticated:
        return BasketProduct.objects.filter(user=request.user)
    else:
        return None

def index(request):
    products = Product.objects.all()
    basket_products = BasketProduct.objects.filter(user__username=request.user)
    brands = WatchBrand.objects.all()

    if request.method == "POST":
        if request.POST.get('basketbtn') == "btnbasket":
            product_id = request.POST.get('product_id')

            product = Product.objects.get(id=product_id)

            if BasketProduct.objects.filter(product=product).exists():
                basket_product = BasketProduct.objects.get(product=product)

                basket_product.adet += 1

                basket_product.save()

                messages.success(request,f'{product} Sepete Eklendi.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))

            else:

                basket_product = BasketProduct.objects.create(user=request.user,product=product,adet=1)

                basket_product.save()
                messages.success(request,f'{product} Sepete Eklendi.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
        
        elif request.POST.get('favoritebtn') == "btnfavorite":
            product_id = request.POST.get('product_id')

            product = Product.objects.get(id=product_id)

            if FavoriteProduct.objects.filter(user=request.user, product=product).exists():

                favorite_product = FavoriteProduct.objects.get(user=request.user, product=product)

                favorite_product.delete()
                
                messages.success(request, f'{product} Favorilerden Çıkartıldı.')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
            else:

                favorite_product = FavoriteProduct.objects.create(user=request.user,product=product)

                favorite_product.save()

                messages.success(request,f'{product} Favorilere Eklendi.')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
    
    context={
        "products":products,
        "basket_products":basket_products,
        "brands":brands,
        "productquantity":ProductQuantity(request)
    }


    return render(request,"index.html",context)


def category(request):
    basket_products = BasketProduct.objects.filter(user__username=request.user)
    products = Product.objects.all().order_by("-id")
    brands = WatchBrand.objects.all()
    genders = WatchGender.objects.all()
    colors = WatchColor.objects.all()
    case_shapes = WatchCaseShape.objects.all()
    strap_types = WatchStrapType.objects.all()
    glass_features = WatchGlassFeature.objects.all()
    styles = WatchStyle.objects.all()
    mechanisms = WatchMechanism.objects.all()
    sepet_product = BasketProduct.objects.all()
    favori_product = FavoriteProduct.objects.all()
    
    filters = Q()

    if 'marka' in request.GET:
        # Birden fazla marka seçilebilir, bu yüzden getlist() yöntemini kullanarak tüm seçimleri alıyoruz
        markalar = request.GET.getlist('marka')
        # Marka seçimlerini Q nesnesine ekliyoruz
        for marka in markalar:
            filters |= Q(marka=marka)

    if 'cinsiyet' in request.GET:
        filters &= Q(cinsiyet=request.GET.get('cinsiyet'))

    if 'renk' in request.GET:
        renkler = request.GET.getlist('renk')

        for renk in renkler:
            filters |= Q(renk=renk)
    
    if 'kasa_sekli' in request.GET:
        kasa_sekilleri = request.GET.getlist('kasa_sekli')

        for kasa_sekli in kasa_sekilleri:
            filters |= Q(kasa_sekli=kasa_sekli)
    
    if 'kayis_tipi' in request.GET:
        kayis_tipleri = request.GET.getlist('kayis_tipi')

        for kayis_tipi in kayis_tipleri:
            filters |= Q(kayis_tipi=kayis_tipi)

    if 'cam_ozellik' in request.GET:
        cam_ozellikleri = request.GET.getlist('cam_ozellik')

        for cam_ozellik in cam_ozellikleri:
            filters |= Q(cam_ozellik=cam_ozellik)

    if 'tarz' in request.GET:
        tarzlar = request.GET.getlist('tarz')

        for tarz in tarzlar:
            filters |= Q(tarz=tarz)

    if 'mekanizma' in request.GET:
        mekanizmalar = request.GET.getlist('mekanizma')

        for mekanizma in mekanizmalar:
            filters |= Q(mekanizma=mekanizma)

        
    
    if 'fiyat_min' in request.GET and 'fiyat_max' in request.GET and request.GET['fiyat_max'] != "":

        fiyat_min = request.GET.get('fiyat_min')
        fiyat_max = request.GET.get('fiyat_max')
        
        # Eğer fiyat_min boşsa, 0 olarak ayarlayın
        if fiyat_min == "":
            fiyat_min = 0

        filters &= Q(fiyat__gte=fiyat_min, fiyat__lte=fiyat_max)

    # Filtreleri kullanarak ürünleri filtrele
        
    products = products.filter(filters).order_by("-id")
    
    paginator = Paginator(products, 1)
    total_products = len(products)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    if request.method == "POST":
        if request.POST.get('basketbtn') == "btnbasket":
            product_id = request.POST.get('product_id')

            product = Product.objects.get(id=product_id)

            if BasketProduct.objects.filter(product=product).exists():
                basket_product = BasketProduct.objects.get(product=product)

                basket_product.adet += 1

                basket_product.save()

                messages.success(request,f'{product} Sepete Eklendi.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'category'))

            else:

                basket_product = BasketProduct.objects.create(user=request.user,product=product,adet=1)

                basket_product.save()
                messages.success(request,f'{product} Sepete Eklendi.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'category'))
        
        elif request.POST.get('favoritebtn') == "btnfavorite":
            product_id = request.POST.get('product_id')

            product = Product.objects.get(id=product_id)

            if FavoriteProduct.objects.filter(user=request.user, product=product).exists():

                favorite_product = FavoriteProduct.objects.get(user=request.user, product=product)

                favorite_product.delete()
                
                messages.success(request, f'{product} Favorilerden Çıkartıldı.')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'category'))
            else:

                favorite_product = FavoriteProduct.objects.create(user=request.user,product=product)

                favorite_product.save()

                messages.success(request,f'{product} Favorilere Eklendi.')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'category'))

    context={
        "products":products,
        "total_products":total_products,
        "brands":brands,
        "genders":genders,
        "colors":colors,
        "case_shapes":case_shapes,
        "strap_types":strap_types,
        "glass_features":glass_features,
        "styles":styles,
        "mechanisms":mechanisms,
        "sepet_product":sepet_product,
        "favori_product":favori_product,
        "basket_products":basket_products,
        "productquantity":ProductQuantity(request)
    }


    return render(request,"category.html",context)


def product_detail(request,slug=None,product_id=None):
    basket_products = BasketProduct.objects.filter(user=request.user)
    product = Product.objects.get(id= product_id)

    context={
        "product":product,
        "basket_products":basket_products,
        "productquantity":ProductQuantity(request)
    }

    return render(request, "product-detail.html", context)


def brands(request):
    brands = WatchBrand.objects.all()
    basket_products = BasketProduct.objects.filter(user=request.user)
    context={
        "brands":brands,
        "basket_products":basket_products,
        "productquantity":ProductQuantity(request)
    }


    return render(request, "brand.html", context)


def sepet(request):
    basket_products = BasketProduct.objects.filter(user=request.user)

    kargo = 29.99
    product_total_price = 0
    for product in basket_products:
        product_total_price = product.adet * product.product.fiyat
    
    total_price = kargo + product_total_price

    if request.method == "POST":
        if request.POST.get('btnplus') == "plusbtn":
            product_id = int(request.POST.get('product_id'))
            print(product_id)

            product_id -= 1

            product = BasketProduct.objects.get(id=product_id)

            product.adet += 1

            product.save()
            return redirect('sepet')
        
        elif request.POST.get('btnminus') == "minusbtn":
            product_id = int(request.POST.get('product_id'))

            product_id += 1

            product = BasketProduct.objects.get(id=product_id)

            product.adet -= 1

            product.save()
            return redirect('sepet')
        
        elif request.POST.get('btndel') == "delbtn":
            product_id = int(request.POST.get('product_id'))


            product = BasketProduct.objects.get(id=product_id)

            product.delete()
            return redirect('sepet')
        
        elif request.POST.get("btncheck") == "checkbtn":

            order = Order.objects.create(user=request.user)

            order.save()
            return redirect('checkout')
    
    request.session['urun_toplam_fiyat'] = product_total_price
    request.session['kargo_ucreti'] = kargo
    request.session['toplam_fiyat'] = total_price

    context={
        "basket_products":basket_products,
        "total_price":total_price,
        "product_total_price":product_total_price,
        "kargo":kargo,
        "productquantity":ProductQuantity(request)
    }

    return render(request, "sepet.html", context)

@login_required(login_url='/login/')
def checkout(request):
    user = User.objects.get(username=request.user)
    profil_info = Profil.objects.get(kullanici=request.user)
    adres = Adres.objects.get(kullanici=request.user)
    basket_products = BasketProduct.objects.filter(user=request.user)
    order = Order.objects.filter(user=request.user).last()


    product_total_price = request.session.get('urun_toplam_fiyat')
    kargo = request.session.get('kargo_ucreti')
    total_price = request.session.get('toplam_fiyat')

    #     CF Başlatma İsteği
    # options = {
    # 'api_key': 'sandbox-QL0n1GUfznJfdZkmzFpfYCgSPdPwUnLc',
    # 'secret_key': 'sandbox-5cBNv3LH8okhFOrDcWADr3jKi34zDV43',
    # 'base_url': 'sandbox-api.iyzipay.com'
    # }

    # if request.method == "POST":
        # Payment Card
        # cardHolderName = request.POST.get("card-name")
        # cardNumber = request.POST.get("card-number")
        # expireMonth = request.POST.get("expiry-month")
        # expireYear = request.POST.get("expiry-year")
        # cvv = request.POST.get("cvv-code")

        # Buyer
        # name = request.POST.get('first-name')
        # surname = request.POST.get('last-name')
        # phonenumber = request.POST.get('phone-number')
        # email = request.POST.get('email')
        # identityNumber = request.POST.get('identityNumber')



        # payment_card = {
        #     'cardHolderName': cardHolderName,
        #     'cardNumber': cardNumber,
        #     'expireMonth': expireMonth,
        #     'expireYear': expireYear,
        #     'cvc': cvv,
        #     'registerCard': '0'
        # }

        # buyer = {
        #     'id': request.user.id,
        #     'name': name,
        #     'surname': surname,
        #     'gsmNumber': phonenumber,
        #     'email': email,
        #     'identityNumber': '74300864791',
        #     'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        #     'ip': request.META.get('REMOTE_ADDR'),
        #     'city': 'Istanbul',
        #     'country': 'Turkey',
        #     'zipCode': '34732'
        # }

        # address = {
        #     'contactName': f'{name} {surname}',
        #     'city': 'Istanbul',
        #     'country': 'Turkey',
        #     'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        #     'zipCode': '34732'
        # }

        # basket_items = []

        # for product in basket_products:
        #     item = {
        #         'id': product.product.id,
        #         'name': product.product.model,
        #         'category1': product.product.marka.brand,
        #         'itemType': "PHYSICAL",
        #         'price': product.product.fiyat * product.adet
        #     }
        #     basket_items.append(item)

        # iyzico_request = {
        #     'locale': 'tr',
        #     'conversationId': order.order_id,
        #     "price": product_total_price,
        #     'paidPrice': total_price,
        #     'currency': 'TRY',
        #     'installment': 1,
        #     'basketId': 'B67832',
        #     'paymentChannel': 'WEB',
        #     'paymentGroup': 'PRODUCT',
        #     "callbackUrl": "http://127.0.0.1:8000/order_success/",
        #     'paymentCard': payment_card,
        #     'buyer': buyer,
        #     'shippingAddress': address,
        #     'billingAddress': address,
        #     'basketItems': basket_items
        # }

        # payment = iyzipay.CheckoutFormInitialize().create(iyzico_request, options)

        # print("Burada",payment.read().decode('utf-8'))
        # json_content = json.loads(payment.read().decode('utf-8'))
        # if json_content['status'] == "success":
        #     return redirect(json_content["paymentPageUrl"]) 

    context={
        "profil_info":profil_info,
        "adres":adres,
        "basket_products":basket_products,
        "total_price":total_price,
        "product_total_price":product_total_price,
        "kargo":kargo,
        "productquantity":ProductQuantity(request)
    }
    
    return render(request,"checkout.html",context)
    

# @csrf_exempt
# def order_success(request):

#     options = {
#     'api_key': 'sandbox-QL0n1GUfznJfdZkmzFpfYCgSPdPwUnLc',
#     'secret_key': 'sandbox-5cBNv3LH8okhFOrDcWADr3jKi34zDV43',
#     'base_url': 'sandbox-api.iyzipay.com'
#     }

#     token = request.session.get('token')
    
#     print(token)
#     payment_request = {
#         'locale': 'tr',
#         'conversationId': request.session.get('order_id'),
#         'token': token
#         }
        
#     checkout_form_result = iyzipay.CheckoutForm().retrieve(payment_request, options)

#     result = checkout_form_result.read().decode('utf-8')

#     print("==",result)

#     return render(request, 'order-success.html')

def favorite(request):
    favori_product = FavoriteProduct.objects.filter(user=request.user)
    basket_products = BasketProduct.objects.filter(user=request.user)

    if request.method == "POST":
        if request.POST.get('basketbtn') == "btnbasket":
                product_id = request.POST.get('product_id')

                product = Product.objects.get(id=product_id)

                if BasketProduct.objects.filter(product=product).exists():
                    basket_product = BasketProduct.objects.get(product=product)

                    basket_product.adet += 1

                    basket_product.save()

                    messages.success(request,f'{product} Sepete Eklendi.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'category'))

                else:

                    basket_product = BasketProduct.objects.create(user=request.user,product=product,adet=1)

                    basket_product.save()
                    messages.success(request,f'{product} Sepete Eklendi.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'category'))
            
        elif request.POST.get('favoritebtn') == "btnfavorite":
            product_id = request.POST.get('product_id')

            product = Product.objects.get(id=product_id)

            if FavoriteProduct.objects.filter(user=request.user, product=product).exists():

                favorite_product = FavoriteProduct.objects.get(user=request.user, product=product)

                favorite_product.delete()
                
                messages.success(request, f'{product} Favorilerden Çıkartıldı.')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'category'))

    context={
        "favori_product":favori_product,
        "basket_products":basket_products,
        "productquantity":ProductQuantity(request)
    }
    
    return render(request,"favorite.html",context)

@login_required(login_url='/login/')
def profil(request):
    user = User.objects.get(username=request.user)
    profil_info = Profil.objects.get(kullanici=user)
    adres = Adres.objects.get(kullanici=user)
    basket_products = BasketProduct.objects.filter(user=request.user)

    if request.method == "POST":
        if request.POST.get('button') == "password":
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            rnew_password = request.POST.get('rnew_password')

            if user.check_password(old_password):
                if new_password == rnew_password:
                    user.set_password(new_password)
                    user.save()
                    logout(request)
                    messages.warning(request, 'Şifreniz Başarılı Bir Şekilde Değiştirildi')
                    return redirect('login')
                else:
                    messages.warning(request, 'Şifreler Uyumsuz. Lütfen Tekrar Deneyiniz.')
            else:
                messages.warning(request, 'Eski Şifreniz Yanlış. Lütfen Tekrar Deneyiniz.')

        elif request.POST.get('button') == "profil":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            tel = request.POST.get('phone_number')
            dogumt = request.POST.get('date_of_birth')

            if user.email != email:
                if not User.objects.filter(email=email).exists():
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    profil_info.telefon_numarasi = tel
                    profil_info.dogum_tarihi = dogumt
                    profil_info.save()
                    user.save()
                    messages.success(request, 'Profil Bilgileriniz Başarılı Bir Şekilde Güncellendi.')
                    return redirect('profil')
                else:
                    messages.warning(request, 'Bu E-Posta Adresi Başka Bir Kullanıcı Tarafından Kullanılıyor.')
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                profil_info.telefon_numarasi = tel
                profil_info.dogum_tarihi = dogumt
                profil_info.save()
                user.save()
                messages.success(request, 'Bilgiler Başarılı Bir Şekilde Güncellendi.')
                return redirect('profil')
        elif request.POST.get('button') == "address":
            il = request.POST.get('il')
            ilce = request.POST.get('ilce')
            mahalle = request.POST.get('mahalle')
            tam_adres = request.POST.get('adres')

            adres.il = il
            adres.ilce = ilce
            adres.mahalle = mahalle
            adres.adres = tam_adres

            adres.save()
            messages.success(request, 'Adres Bilgileriniz Başarılı Bir Şekilde Güncellendi.')
            return redirect('profil')




    context={
        "profil_info":profil_info,
        "adres":adres,
        "basket_products":basket_products,
        "productquantity":ProductQuantity(request)
    }
    
    return render(request,"user/profil.html", context)


def search(request):

    if "search" in request.GET and request.GET["search"] != "":
        search = request.GET["search"]
    
    return render(request,"category.html")

def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user is not None:
                    login(request,user)
                    return redirect("index")
                else:
                    messages.error(request, "Bu Bilgilere Ait Bir Kullanıcı Bulunamadı. Lütfen Tekrar Deneyin.")
            else:
                messages.error(request, "Şifreniz Yanlış. Lütfen Tekrar Deneyin.")
        else:
            messages.error(request, "E-Posta Adresiniz Yanlış. Lütfen Tekrar Deneyin.")
                    

    return render(request, "user/login.html")

def Register(request):
    if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            if len(password) >= 6:
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create(username=email,first_name=first_name,last_name=last_name,email=email,password=password)
                    user.save()
                    login(request,user)
                    return redirect("index")
                else:
                    messages.error(request, "Bu E-Mail Başka Bir Kullanıcı Tarafından Kullanılıyor.")
            else:
                messages.error(request, "Şifre En Az Altı Karakterden Oluşmalıdır.")

    return render(request, "user/register.html")

def Logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
