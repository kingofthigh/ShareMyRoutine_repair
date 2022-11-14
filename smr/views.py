from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.core.paginator import Paginator
from django.views.generic.edit import ModelFormMixin

from django.contrib.contenttypes.models import ContentType
from braces.views import LoginRequiredMixin
from allauth.account.views import PasswordChangeView

from .mixins import LoginAndVerificationRequiredMixin, LoginAndOwnershipRequiredMixin
from .models import Post, Wkout, WkRecord, User, Profile, Comment, Like, Copy
from .forms import WkoutMemoForm, WkRecordForm, PostForm, ProfileForm, CommentForm

import datetime
# Create your views here.


# 인덱스 - 메인 페이지
# 필요한 데이터: 로그인한 유저, 그 유저가 팔로잉하는 사람, 그 사람의 post 데이터

class index(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'smr/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author__followers__id=self.request.user.id)
        # 포스터 중, '포스터'의 '게시자'를 '팔로우'하는 사람이 현재 접속한 '유저'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time = datetime.datetime.now()
        time = time.date()
        userWkoutExist = Wkout.objects.filter(author=self.request.user).filter(dt_created__contains=time)
        # 운동 일지(Wkout) 중, '작성자'가 현재 접속한 '유저'이고, '생성날짜'가 오늘인 '운동 일지'
        if userWkoutExist:
            context['wkout_exist'] = userWkoutExist[0]
        else:
            context['wkout_exist'] = None
        return context
        # 추가 데이더, 현재 접속한 유저의 운동일지 생성 여부

        
    




# 운동 일지 목록
class WkoutListView(LoginRequiredMixin, ListView):
    model = Wkout
    tmeplate_name = "smr/wkout_list.html"
    context_object_name = "wkouts"

    def get_queryset(self):
        return Wkout.objects.filter(author__id=self.request.user.id)
    # 현재 접속한 '유저'의 '운동일지'
    def get_context_data(self, **kwargs):
        time = datetime.datetime.now()
        time = time.date()
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author__followers__id=self.request.user.id).filter(dt_created__contains=time)
        context["posts"] = posts 
        return context
        # 추가 데이터, '포스터' 중 현재 접속한 '유저'가 '팔로우'한 '유저' 오늘 작성한 '포스터'
    

class WkoutCreateView(LoginRequiredMixin, CreateView):
    model = Wkout
    form_class = WkoutMemoForm
    template_name = 'smr/memo_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("wkrecord-list", kwargs={"wkout_id": self.object.id})
    # 운동일지 작성 폼
    # 작성 완료 후, 운동 세트 기록 페이지(운동일지 내)로 이동


class WkoutUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Wkout
    form_class = WkoutMemoForm
    template_name = "smr/wkout_update_form.html"
    pk_url_kwarg = "wkout_id"

    def get_success_url(self):
        return reverse('wkrecord-list', kwargs={"wkout_id": self.object.id })
    # 운동일지 업데이트 폼
    # 작성 완료 후, 운동 세트 기록 페이지(운동일지 내)로 이동

class WkoutDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Wkout
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('wkout-list')



    # 운동일지 삭제 폼
    # 삭제 후 
    

# 운동 기록 작성 
class WkRecordCreateView(LoginRequiredMixin, CreateView):
    model = WkRecord
    form_class = WkRecordForm
    template_name = "smr/wkrecord_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wkrecord = WkRecord.objects.filter(wkout__id=self.kwargs.get('wkout_id'))
        context['wkrecords'] = wkrecord

        volume = 0
        for vol in wkrecord:
            volume += vol.weight * vol.reps
        context["total_vol"] = volume
        
        wkout = Wkout.objects.get(id=self.kwargs.get('wkout_id'))
        context['wkout'] = wkout
        return context
    
    def form_valid(self, form):
        form.instance.wkout = Wkout.objects.get(id=self.kwargs.get('wkout_id'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('wkrecord-list', kwargs={"wkout_id": self.kwargs.get('wkout_id')})
    

class WkRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = WkRecord
    form_class = WkRecordForm
    template_name = "smr/wkrecord_update_form.html"
    pk_url_kwarg = "wkrecord_id"

    def get_success_url(self):
        return reverse('wkrecord-list', kwargs={"wkout_id": self.object.wkout.id })


class WkRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = WkRecord

    def get_success_url(self):
        return reverse('wkrecord-list', kwargs={'wkout_id': self.object.wkout.id})



# 포스트 관련

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'smr/user_post_list.html'
    context_object_name = 'user_posts'
    # paginate_by = 15

    def get_queryset(self):
        return Post.objects.filter(author__id=self.kwargs.get('user_id'))
    
    
class PostAllListView(LoginRequiredMixin, ListView):
    model = Post
    tmeplate_name = 'smr/post_list.html'
    context_object_name = 'posts'
    # paginate_by = 20
    

# class PostDetailView(LoginRequiredMixin, DetailView):
#     model = Post
#     template_name = 'smr/post_detail.html'
#     pk_url_kwarg = 'post_id'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         wkout = self.object.wkout
#         # 포스트 운동 기록 리스트
#         context["wkrecords"] =  WkRecord.objects.filter(wkout=wkout)
#         context["form"] = CommentForm()
#         # 좋아요 용 contenttype
#         context["post_ctype_id"] = ContentType.objects.get(model='post').id
#         context["comment_ctype_id"] = ContentType.objects.get(model='comment').id

#         user = self.request.user
#         post = self.object
#         context['likes_post'] = Like.objects.filter(user=user, post=post).exists()
#         context['liked_comments'] = Comment.objects.filter(post=post).filter(likes__user=user)
#         time = datetime.datetime.now()
#         time = time.date()
        
#         #오늘자 운동 기록페이지 만들었는 지 확인
#         userWkoutExist = Wkout.objects.filter(author=user).filter(dt_created__contains=time)
        
#         if userWkoutExist:
#             context['wkout_exist'] = userWkoutExist[0]
#             copy_list = Copy.objects.filter(wkout_id=userWkoutExist[0].id).filter(copy_post__wkout__id=self.object.wkout.id)
#             context["copy_list"] = copy_list
#         else:
#             context['wkout_exist'] = None
#         return context
    
#     def post(self, request, *args, **kwargs):
#         post = Post.objects.get(id=self.kwargs.get('post_id'))
#         user = self.request.user
#         form = CommentForm(data=request.POST)
#         if form.is_valid():
#             form.instance.post = post
#             form.instance.author = user
#             form.save()
#         return redirect('post-detail', post_id=self.kwargs.get('post_id'))
        # return self.get(request, *args, **kwargs)

class PostDetailView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'smr/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        context['post'] = post

        wkout = post.wkout
        # 포스트 운동 기록 리스트
        context["wkrecords"] =  WkRecord.objects.filter(wkout=wkout)
        # 좋아요 용 contenttype
        context["post_ctype_id"] = ContentType.objects.get(model='post').id
        context["comment_ctype_id"] = ContentType.objects.get(model='comment').id

        user = self.request.user
        context['likes_post'] = Like.objects.filter(user=user, post=post).exists()
        context['liked_comments'] = Comment.objects.filter(post=post).filter(likes__user=user)
        time = datetime.datetime.now()
        time = time.date()
        
        #오늘자 운동 기록페이지 만들었는 지 확인
        userWkoutExist = Wkout.objects.filter(author=user).filter(dt_created__contains=time)
        
        if userWkoutExist:
            context['wkout_exist'] = userWkoutExist[0]
            copy_list = Copy.objects.filter(wkout_id=userWkoutExist[0].id).filter(copy_post__wkout__id=self.object.wkout.id)
            context["copy_list"] = copy_list
        else:
            context['wkout_exist'] = None
        return context

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs.get('post_id'))
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.kwargs.get('post_id')})

class PostCreateView(LoginAndVerificationRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "smr/post_create_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wkout = Wkout.objects.get(id=self.kwargs['wkout_id'])
        context['wkout'] = wkout
        return context

    def form_valid(self, form):
        wkout = Wkout.objects.get(id=self.kwargs.get('wkout_id'))
        form.instance.author = self.request.user
        form.save(commit=False)
        form.instance.wkout = wkout
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("post-detail", kwargs={"post_id": self.object.id})
    

class PostDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PostUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "smr/post_create_form.html"
    pk_url_kwarg = "post_id"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"post_id": self.object.id})



# 프로필 페이지

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "smr/profile.html"
    pk_url_kwarg = "user_id"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile_user_id = self.kwargs.get('user_id')
        context['is_following'] = user.following.filter(id=profile_user_id).exists()
        context['followings'] = User.objects.filter(followers__id=profile_user_id)
        context['followers'] = User.objects.filter(following__id=profile_user_id)
        return context

class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "smr/profile_set_form.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('index')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "smr/profile_update_form.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile', kwargs=({"user_id": self.request.user.id}))
        

# comment

class CommentDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.post.id})

class CommentUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        return Comment.objects.get(id=self.kwargs.get('pk'))
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.post.id})


# 좋아요

class ProcessLikeView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        like, created = Like.objects.get_or_create(
            user=self.request.user,
            content_type_id=self.kwargs.get('content_type_id'),
            object_id=self.kwargs.get('object_id'),
        )
        if not created:
            like.delete()
        
        return redirect(self.request.META['HTTP_REFERER'])

# 팔로우

class ProcessFollowView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile_user_id = self.kwargs.get('user_id')
        if user.following.filter(id=profile_user_id).exists():
            user.following.remove(profile_user_id)
        else:
            user.following.add(profile_user_id)
        return redirect('profile', user_id=profile_user_id)


class CopyWkoutView(LoginRequiredMixin, View):

    
    def post(self, request, *args, **kwargs):
        wkout = WkRecord.objects.filter(wkout__id=self.kwargs.get('wkout_id')) # 운동 기록 한세트들의 모임
        recent_wkout_page = Wkout.objects.filter(author=self.request.user)[0]
        time = datetime.datetime.now()
        time = time.date()
        

        # 오늘 만든 운동 작성일지가 있을 때
        if recent_wkout_page.dt_created.date() == time:
            # 카피 테이블에 현재 포스트의 운동일지와 내가 오늘 만든 운동 일지가 없는 경우에만 카피한다.
            copy = Copy.objects.create(
                wkout=Wkout.objects.filter(author=self.request.user)[0],
                copy_post=Post.objects.get(wkout__id=self.kwargs.get("wkout_id"))
            )
            for wkrecord in wkout:
                wkr = WkRecord.objects.create(
                    wkout=Wkout.objects.filter(author=self.request.user)[0],
                    exercise=wkrecord.exercise,
                    weight=wkrecord.weight,
                    reps=wkrecord.reps,
                )
                wkr.save()
            #저장 후 해당 wkout 페이지로 이동
            return redirect('wkrecord-list', wkout_id=recent_wkout_page.id )
            # 있을 경우 
        else:
            return redirect('copy-wkout-create')

class CopyWkoutCreateView(LoginRequiredMixin, CreateView):
    model = Wkout
    form_class = WkoutMemoForm
    template_name = 'smr/copy_wkout_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wkout = Wkout.objects.get(id=self.kwargs.get('wkout_id'))
        context["wkout"] = wkout
        post = Post.objects.get(wkout_id=wkout.id)
        context['post'] = post 
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        post = Post.objects.get(wkout__id=self.kwargs.get('wkout_id'))
        return reverse('post-detail', kwargs={"post_id": post.id})
    
    

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs=({"user_id": self.request.user.id}))

