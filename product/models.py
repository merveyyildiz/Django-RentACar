from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class Category(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()  # id yerine metin ile çağırmak istersek
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',
                               on_delete=models.CASCADE)  # cascade eğer bu tablo silinirse buna bağlı şeylerde silinsin,self dedğimiz için sadece kendi kendine ilişkisi var
    create_at = models.DateTimeField(auto_now_add=True)  # oluşturulma zmanını tutar
    update_At = models.DateTimeField(auto_now=True)

    def image_tag(self):  # bu fonskiyonu admin kısmında resimler gözüksün diye yazıyoruz ve bu fonk artık çağıracağız
        return mark_safe('<img src= "{}" height="50"/>'.format(
            self.image.url))  # süslü parantezler içine image url gönderdik. oda admin sayfasında img tag ile gözükmesini sağlar

    def __str__(self):
        return self.title


class Car(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # category ile ilişkisi var
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')  # images klasörüne kaydet
    price = models.FloatField()
    amount = models.IntegerField()
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):  # bu fonskiyonu admin kısmında resimler gözüksün diye yazıyoruz ve bu fonk artık çağıracağız
        return mark_safe('<img src= "{}" height="50"/>'.format(
            self.image.url))  # süslü parantezler içine image url gönderdik. oda admin sayfasında img tag ile gözükmesini sağlar

    image_tag.short_description = 'Image'


class Images(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):  # bu fonskiyonu admin kısmında resimler gözüksün diye yazıyoruz ve bu fonk artık çağıracağız
        return mark_safe('<img src= "{}" height="50"/>'.format(
            self.image.url))  # süslü parantezler içine image url gönderdik. oda admin sayfasında img tag ile gözükmesini sağlar

    image_tag.short_description = 'Image'
