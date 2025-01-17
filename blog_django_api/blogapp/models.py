from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    bio=models.TextField(blank=True,null=True)
    profile=models.ImageField(upload_to='profile_image',blank=True,null=True)
    twitter=models.URLField(max_length=200,blank=True,null=True)
    linkedin=models.URLField(max_length=200,blank=True,null=True)
    instagram=models.URLField(max_length=200,blank=True,null=True)
    portfolio=models.URLField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return self.username

class Blog(models.Model):
    CATEGORY= (
        ("Technology","Technology"),
        ("Economy","Economy"),
        ("Businesss","Businesss"),
        ("Sports","Sports"),
        ("Lifestyles","Lifestyles"),
        
    )
    title=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,unique=True,blank=True)
    content=models.TextField()
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="blogs",null=True)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)
    #  created_time=models.DateTimeField(format="%Y-%m-%d")
    # updated_time=models.DateTimeField(format="%Y-%m-%d")
    published_time=models.DateField(blank=True,null=True)
    is_draft_pub=models.BooleanField(default=True)
    category=models.CharField(max_length=255,choices=CATEGORY,blank=True,null=True)
    thumbnail=models.ImageField(upload_to="blog_img",blank=True,null=True)
    
    class Meta:
        ordering=["-published_time"]
    
    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        base_slug=slugify(self.title)
        slug=base_slug
        num=1
        while Blog.objects.filter(slug=slug).exists():
            slug=f'{base_slug}--{num}'
            num += 1
        self.slug=slug
            
        if not self.is_draft_pub and self.published_time is None:
            self.published_time=timezone.now().date()
        super().save(*args,**kwargs)
        