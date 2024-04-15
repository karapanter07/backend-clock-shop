from django.contrib import admin
from .models import *
from reversion.admin import VersionAdmin

admin.site.register(Product)
admin.site.register(Profil)
admin.site.register(Adres)
admin.site.register(WatchBrand)
admin.site.register(WatchCaseShape)
admin.site.register(WatchColor)
admin.site.register(WatchGender)
admin.site.register(WatchGlassFeature)
admin.site.register(WatchMechanism)
admin.site.register(WatchStrapType)
admin.site.register(WatchStyle)
admin.site.register(BasketProduct)
admin.site.register(FavoriteProduct)
admin.site.register(Order)
