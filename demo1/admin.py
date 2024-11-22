from django.contrib import admin
from demo1.models import User, Country_Codes, District, Franchise_Type, State, Franchisee


# Register your models here.

admin.site.register(User)
admin.site.register(Franchisee)
admin.site.register(Franchise_Type)
admin.site.register(State)
admin.site.register(Country_Codes)
admin.site.register(District)