from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver


from .validators import validate_no_special_characters, weight_validator, percentage


# Create your models here.
class User(AbstractUser):

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name="followers"
    )

    likes = GenericRelation('Like')

    def __str__(self):
        return self.username

class Profile(models.Model):
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={"unique":"이미 사용중인 닉네임입니다."},
    )
    career = models.FloatField(null=True)
    profile_pic = models.ImageField(
        default="default_profile_pic.jpg", upload_to="profile_pics"
    )
    intro = models.CharField(max_length=60, blank=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    muscle_mass = models.FloatField(blank=True, null=True)
    body_fat = models.FloatField(blank=True, null=True, validators=[percentage])
    squat = models.FloatField(blank=True, null=True, validators=[weight_validator])
    deadlift = models.FloatField(blank=True, null=True, validators=[weight_validator])
    benchpress = models.FloatField(blank=True, null=True, validators=[weight_validator])

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    
    
    



class Part(models.Model):
    partname = models.CharField(max_length=30)

    def __str__(self):
        return self.partname

class Exercise(models.Model):
    exname = models.CharField(max_length=30)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="exercises")

    def __str__(self):
        return self.exname

class Wkout(models.Model):
    memo = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wkouts")
    dt_created = models.DateTimeField(auto_now_add=True)
    EXPART = [
        ('가슴', '가슴'),
        ('등', '등'),
        ('하체', '하체'),
        ('어깨', '어깨'),
        ('팔', '팔'),
        ('복근', '복근'),
        ('상체', '상체'),
        ('밀기', '밀기'),
        ('당기기', '당기기'),
        ('전신', '전신'),
    ]
    ex_part = models.CharField(max_length=10, choices=EXPART, blank=True)

    def __str__(self):
        return str(self.memo[:15])
    class Meta:
        ordering = ['-dt_created']

class WkRecord(models.Model):
    wkout = models.ForeignKey(Wkout, on_delete=models.CASCADE, related_name="wkrecords")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    dt_created = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(default=0, validators=[weight_validator])
    reps = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['dt_created']
    
    def __str__(self):
        return str(self.wkout) + '/' + str(self.exercise)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    dt_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to="pics", blank=True)
    wkout = models.OneToOneField(Wkout, on_delete=models.CASCADE)

    likes = GenericRelation('Like', related_query_name='post')

    def __str__(self):
        return str(self.content[:10])
    
    class Meta:
        ordering = ['-dt_created']


class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    likes = GenericRelation('Like', related_query_name='comment')

    def __str__(self):
        return self.content[:20]
    class Meta:
        ordering = ['-dt_created']

class Like(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"({self.user}, {self.liked_object})"
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
    #제네릭 외래키는 거의 남의 pk 2개로 만든 pk?느낌 근데 이름이 기억이 안나네 

class Copy(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)

    wkout = models.ForeignKey(Wkout, on_delete=models.CASCADE, related_name="copys")
    copy_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="copys")

    class Meta:
        unique_together = ['wkout', 'copy_post']
    
    def __str__(self):
        return str(self.wkout) + '/' + str(self.copy_post.wkout)