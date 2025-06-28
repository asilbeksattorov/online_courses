from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    duration = models.TimeField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_courses', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='course/images')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class ItemBase(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Text(ItemBase):
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Video(ItemBase):
    url = models.URLField()
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.title


class Image(ItemBase):
    image = models.FileField(upload_to='images/')

    def __str__(self):
        return self.title


class File(ItemBase):
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.title


# class Topic(models.Model): # Content Type
#     pass
#     # file = models.ForeignKey(File)
#     # text = models.ForeignKey(Text)
#     # video = models.ForeignKey(Video)
#     # image = models.ForeignKey(Image)


class Topic(models.Model):
    module = models.ForeignKey(Module,
                               related_name='topics',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file',
                                     )}
                                     )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['my_order']





# class Role(models.Model):
#     name = models.CharField(max_length=200,unique=True)

#     def __str__(self):
#         return self.name


# class CustomUser(AbstractUser):
#     email = models.EmailField()
#     phone_number = models.CharField()
#     role = models.ForeignKey(Role,related_name='users',on_delete=models.CASCADE)




class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value,
                                              null=True, blank=True)
    content = models.TextField()
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True
    )
    video_id = models.ForeignKey(Video, on_delete=models.SET_NULL, related_name='comments', null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'{self.video_id} - {self.user_id}'

    def get_replies(self):
        return self.replies.all()