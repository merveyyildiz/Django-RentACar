from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.
from django.utils.safestring import mark_safe


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)  # id yerine metin ile çağırmak istersek
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children',
                               on_delete=models.CASCADE)  # cascade eğer bu tablo silinirse buna bağlı şeylerde silinsin,self dedğimiz için sadece kendi kendine ilişkisi var
    create_at = models.DateTimeField(auto_now_add=True)  # oluşturulma zmanını tutar
    update_At = models.DateTimeField(auto_now=True)

    def image_tag(self):  # bu fonskiyonu admin kısmında resimler gözüksün diye yazıyoruz ve bu fonk artık çağıracağız
       return mark_safe('<img src= "{}" height="50"/>'.format(self.image.url))  # süslü parantezler içine image url gönderdik. oda admin sayfasında img tag ile gözükmesini sağlar

    def get_absolute_url(self): #otomatik slug oluşturma
        return reverse('category_detail', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self): #alt kategorileri arıyor ve getiriyor
        full_path=[self.title]
        k= self.parent
        while k is not None:
            full_path.append(k.title)
            k= k.parent
        return ' -> '.join(full_path[::-1])


class Car(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # category ile ilişkisi var
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')  # images klasörüne kaydet
    price = models.FloatField()
    amount = models.IntegerField()
    slug = models.SlugField(blank=True, max_length=150)
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

    def get_absolute_url(self):  # otomatik slug oluşturma
        return reverse('car_detail', kwargs={'slug': self.slug})

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
class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # category ile ilişkisi var
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10,blank=True, choices=STATUS,default='new')
    create_at = models.DateTimeField(auto_now_add=True)
    update_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields= ['subject','comment' ,'rate'] #hangi alanları html de çağıracaksak bunları belirtiyoruz

