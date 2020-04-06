from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Setting, user, comment anasayfayı ilgilendirdiği için burda tanımladık
from django.forms import TextInput, Textarea, ModelForm


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtpserver = models.CharField(blank=True, max_length=20)
    smtpemail = models.CharField(blank=True, max_length=20)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')  # blank true boş bırakabilir sağlıyor
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    abotus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)  # oluşturulma zmanını tutar
    update_At = models.DateTimeField(auto_now=True)

    def __str__(self):  # adı gözüksün return ettiğinde
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ("New", 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=50)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.CharField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default="new")
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # adı gözüksün return ettiğinde
        return self.name


class ContactFormu(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message'] #bu alanların doldurulmasını istiyoruz
        widgets = {
            'name': TextInput(attrs={'class': 'name-input', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'subject-input', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'email-input', 'placeholder': 'Enter Email'}),
            'message': Textarea(attrs={'class': 'textarea', 'placeholder': 'Your message', 'rows': '5'}),
        }
