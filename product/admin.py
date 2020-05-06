from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from product.models import Category, Car, Images,Comment

class CarImageInline(admin.TabularInline):
    model = Images
    extra = 5  # image tablosundan 5 tane alan oluştur


class CategoryAdmin(admin.ModelAdmin):
    #fields = ['title', 'status','image'] # herhangi bir categoriye tıklandığında ekleme silme düzenleme için alnaları gösterir
    list_display = ['title', 'status', 'image_tag']  # categori sayfasında katedorinin özelliklerinden bunları göster
    readonly_fields = ('image_tag',)
    list_filter = ["status"]  # filtreleme

class CarAdmin(admin.ModelAdmin):
    # fields = ['title', 'status'] ekleme silme düzenleme için alanlari gösterir
    list_display = ['title', 'category', 'price','image_tag',
                    'status']  # 'image' eklersek image yolunu verir, image_tag fonk çağırdık resim gözüksün diye
    readonly_fields = ('image_tag',)
    list_filter = ["status", "category"]  # filtreleme
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CarImageInline]  # burada çağırdığımız için sadece ilgili olanları ekler

class ImageAdmin(admin.ModelAdmin):
    # fields = ['title', 'status'] ekleme silme düzenleme için alanaları gösterir
    list_display = ['title', 'car', 'image_tag']
    readonly_fields = ('image_tag',)

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Car,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Car,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'car','user','status']
    list_filter = ['status',]

admin.site.register(Car, CarAdmin)
admin.site.register(Category, CategoryAdmin2)
admin.site.register(Images, ImageAdmin)  # imageadmindeki şablona uy
admin.site.register(Comment, CommentAdmin)