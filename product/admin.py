from django.contrib import admin

# Register your models here.
from product.models import Category, Car, Images

class CarImageInline(admin.TabularInline):
    model = Images
    extra = 5  # image tablosundan 5 tane alan oluştur


class CategoryAdmin(admin.ModelAdmin):
    # fields = ['title', 'status'] # herhangi bir categoriye tıklandığında ekleme silme düzenleme için alnaları gösterir
    list_display = ['title', 'status', 'image_tag']  # categori sayfasında katedorinin özelliklerinden bunları göster
    readonly_fields = ('image_tag',)
    list_filter = ["status"]  # filtreleme

class CarAdmin(admin.ModelAdmin):
    # fields = ['title', 'status'] ekleme silme düzenleme için alanlari gösterir
    list_display = ['title', 'category', 'price', 'image_tag',
                    'status']  # 'image' eklersek image yolunu verir, image_tag fonk çağırdık resim gözüksün diye
    readonly_fields = ('image_tag',)
    list_filter = ["status", "category"]  # filtreleme
    inlines = [CarImageInline]  # burada çağırdığımız için sadece ilgili olanları ekler

class ImageAdmin(admin.ModelAdmin):
    # fields = ['title', 'status'] ekleme silme düzenleme için alanaları gösterir
    list_display = ['title', 'car', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Car, CarAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Images, ImageAdmin)  # imageadmindeki şablona uy