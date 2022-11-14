from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import User, Profile, Wkout, Part, Exercise, WkRecord, Post, Comment, Like
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment

class LikeInline(GenericStackedInline):
    model = Like

class WkRecordInline(admin.StackedInline):
    model = WkRecord

class UserInline(admin.StackedInline):
    model = User.following.through
    fk_name = 'to_user'
    verbose_name = 'Follower'
    verbose_name_plural = 'Followers'

admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += (('Custom fields', {'fields':('following',)}),)
UserAdmin.inlines = (UserInline,)




admin.site.register(Part)

admin.site.register(Exercise)

class WkoutAdmin(admin.ModelAdmin):
    inlines = (
        WkRecordInline,
    )
admin.site.register(Wkout, WkoutAdmin)

admin.site.register(WkRecord)

class PostAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
        LikeInline,
    )

admin.site.register(Post, PostAdmin)

admin.site.register(Profile)

class CommentAdmin(admin.ModelAdmin):
    inlines = (
        LikeInline,
    )
admin.site.register(Comment, CommentAdmin)

admin.site.register(Like)