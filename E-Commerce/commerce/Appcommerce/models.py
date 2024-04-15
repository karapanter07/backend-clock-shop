from django.db import models
from django.contrib.auth.models import User
import uuid
import secrets
import string
class WatchBrand(models.Model):
    brand = models.CharField(max_length=50)
    image = models.ImageField(upload_to="Marka Fotoğrafları", null=True)

    def __str__(self):
        return self.brand
    
    class Meta:
        verbose_name_plural = "Markalar"
    
class WatchGender(models.Model):
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.gender
    
    class Meta:
        verbose_name_plural = "Cinsiyetler"

class WatchColor(models.Model):
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.color
    class Meta:
        verbose_name_plural = "Renkler"

class WatchCaseShape(models.Model):
    case_shape = models.CharField(max_length=50)

    def __str__(self):
        return self.case_shape
    
    class Meta:
        verbose_name_plural = "Kasa Şekilleri"
    
class WatchStrapType(models.Model):
    strap_type = models.CharField(max_length=50)

    def __str__(self):
        return self.strap_type
    
    class Meta:
        verbose_name_plural = "Kayış Tipleri"
    
class WatchGlassFeature(models.Model):
    glass_feature = models.CharField(max_length=50)

    def __str__(self):
        return self.glass_feature
    
    class Meta:
        verbose_name_plural = "Cam Özellikleri"
    
class WatchStyle(models.Model):
    style = models.CharField(max_length=50)

    def __str__(self):
        return self.style
    
    class Meta:
        verbose_name_plural = "Tarzlar"
    
class WatchMechanism(models.Model):
    mechanism = models.CharField(max_length=50)

    def __str__(self):
        return self.mechanism
    
    class Meta:
        verbose_name_plural = "Mekanizmalar"

class Product(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    marka = models.ForeignKey(WatchBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=250)
    aciklama = models.TextField()
    fotograf = models.ImageField(upload_to="Ürün Fotoğrafları")
    fiyat = models.FloatField()
    cinsiyet = models.ForeignKey(WatchGender, on_delete=models.CASCADE)
    renk = models.ForeignKey(WatchColor, on_delete=models.CASCADE)
    kasa_sekli = models.ForeignKey(WatchCaseShape, on_delete=models.CASCADE)
    kayis_tipi = models.ForeignKey(WatchStrapType, on_delete=models.CASCADE)
    cam_ozellik = models.ForeignKey(WatchGlassFeature, on_delete=models.CASCADE)
    tarz = models.ForeignKey(WatchStyle, on_delete=models.CASCADE)
    mekanizma = models.ForeignKey(WatchMechanism, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.marka}-{self.model}'
    
    class Meta:
        verbose_name_plural = "Ürünler"

class BasketProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    adet = models.IntegerField()

    def __str__(self):
        return f'{self.user}-{self.product.model}'

    class Meta:
        verbose_name_plural = "Sepetteki Ürünler"

class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}-{self.product.model}'

    class Meta:
        verbose_name_plural = "Favori Ürünler"

class Adres(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    adres = models.TextField(null=True,blank=True)
    il = models.CharField(max_length=50,null=True,blank=True)
    ilce = models.CharField(max_length=50,null=True,blank=True)
    mahalle = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return f'{self.kullanici}'
    
    class Meta:
        verbose_name_plural = "Adresler"

class Profil(models.Model):
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon_numarasi = models.CharField(max_length=50, null=True,blank=True)
    dogum_tarihi = models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.kullanici)
    
    class Meta:
        verbose_name_plural = "Profiller"

class Order(models.Model):
    order_id = secrets.token_hex(16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Siparişler"
