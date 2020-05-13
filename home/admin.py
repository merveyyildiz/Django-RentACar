from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage, UserProfile, OrderProduct, Order, Faq


class ContactFromMessageAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','message','note','status']
    list_filter=["status"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone', 'address', 'city', 'county', 'image_tag',]


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'date_buy',)
    can_delete = False  # silinmesin
    extra = 0  # ekstra satır olmasın

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'total', 'status','car_id']
    list_filter = ['status']
    readonly_fields = ('user', 'address', 'city', 'country', 'phone', 'first_name', 'ip',
                       'total','date_buy','quatity','car_id')  # sadece okunabiliyor bu bilgiler değiştirilemez
    can_delete = False  # silinmesin
    inlines = [OrderProductline]  # aynı satırda gözükmesi için


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price']
    list_filter = ['user']

class FaqAdmin(admin.ModelAdmin):
    list_display = ['ordernmbr','question', 'answer', 'status']
    list_filter = ['status']

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(ContactFormMessage, ContactFromMessageAdmin)
admin.site.register(Setting)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Faq,FaqAdmin)