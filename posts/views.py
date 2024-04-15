from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DeleteView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from taggit.models import Tag

from posts.forms import ContactForm, CommentForm, PostCreateForm
from posts.models import Posts, Category, Comment



def get_hitcount(request, object):
    hit_count = get_hitcount_model().objects.get_for_object(object)
    hits = hit_count.hits
    context = {}
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    return hitcontext



def pagination(request, objects):
    page_size = request.GET.get('page_size', 4)
    paginator = Paginator(objects, page_size)

    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    return page_obj





class HomePageView(ListView):
    model = Posts
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Posts.published.all().order_by("-published_at")[:3]
        context['most_viewed'] = sorted(Posts.published.all(), key=lambda a: a.get_hit_count, reverse=True)[:3]
        context['recommended'] = Posts.published.all().filter(recommended=True)[:3]
        last_week_posts = Posts.objects.filter(published_at__gte=timezone.now()-timezone.timedelta(days=7))
        last_month_posts = Posts.objects.filter(published_at__gte=timezone.now()-timezone.timedelta(days=30))
        context['popular_posts_week'] = sorted(last_week_posts, key=lambda a: a.get_hit_count, reverse=True)[:3]
        context['popular_posts_month'] = sorted(last_month_posts, key=lambda a: a.get_hit_count, reverse=True)[:6]
        return context


class AboutPageView(View):
    def get(self, request):
        return render(request, 'blog/about.html')


class LatestPostsView(View):
    def get(self, request):
        posts = Posts.published.all().order_by('-published_at')[:10]

        page_obj = pagination(request, posts)
        return render(request, 'blog/latest_posts.html',{'page_obj': page_obj})


class ContactPageView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'blog/contact.html', {'from': form})

    def post(self, request):
        form = ContactForm(data=request.POST)

        if request.method == 'POST' and form.is_valid():
            form.save()
            messages.success(request, "Biz bilan bog'langaningiz uchun tashakkur!")

        return render(request, 'blog/contact.html', {'from': form})



class CPlusView(View):
    def get(self, request):
        posts = Posts.objects.filter(category__name='C++').order_by('-published_at')

        page_obj = pagination(request, posts)
        return render(request, 'blog/C++.html', {'page_obj': page_obj})


class PythonView(View):
    def get(self, request):
        posts = Posts.objects.filter(category__name='Python').order_by('-published_at')

        page_obj = pagination(request, posts)
        return render(request, 'blog/python.html', {'page_obj': page_obj})



class PHPView(View):
    def get(self, request):
        posts = Posts.objects.filter(category__name='PHP').order_by('-published_at')

        page_obj = pagination(request, posts)
        return render(request, 'blog/PHP.html', {'page_obj': page_obj})



class JavaScriptView(View):
    def get(self, request):
        posts = Posts.objects.filter(category__name='JavaScript').order_by('-published_at')

        page_obj = pagination(request, posts)
        return render(request, 'blog/javascript.html', {'page_obj': page_obj})



class CSSView(View):
    def get(self, request):
        posts = Posts.objects.filter(category__name='CSS').order_by('-published_at')

        page_obj = pagination(request, posts)
        return render(request, 'blog/CSS.html', {'page_obj': page_obj})



class ProgrammingView(View):
    def get(self, request):
        posts = Posts.objects.filter(category__name="Dasturlashni o'rganish").order_by('-published_at')

        page_obj = pagination(request, posts)
        return render(request, 'blog/programming.html', {'page_obj': page_obj})


class HostingView(View):
    def get(self, request):
        posts = Posts.objects.filter(category__name='Hosting').order_by('-published_at')

        page_obj = pagination(request, posts)
        return render(request, 'blog/hosting.html', {'page_obj': page_obj})



class OtherInformView(View):
    def get(self, request):
        posts = Posts.objects.filter(category__name="Boshqa ma'lumotlar").order_by('-published_at')

        page_obj = pagination(request, posts)
        return render(request, 'blog/another.html', {'page_obj': page_obj})




class PostDetailView(View):
    def get(self, request, id):
        post = Posts.objects.get(id=id)
        form = CommentForm()

        context = get_hitcount(request, post)
        context['post'] = post
        context['form'] = form

        return render(request, 'blog/post_detail.html', context)



class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostCreateForm()
        categories = Category.objects.all()
        return render(request, 'crud/post_create.html', {'form': form, 'categories': categories})

    def post(self, request):
        form = PostCreateForm(
            data=request.POST,
            files=request.FILES
        )
        categories = Category.objects.all()

        if form.is_valid():
            Posts.objects.create(
                author=self.request.user,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                tags=form.cleaned_data['tags'],
                image=form.cleaned_data['image'],
                category=form.cleaned_data['category']
            )
            return redirect('my_posts')
        return render(request, 'crud/post_create.html', {'form': form, 'categories': categories})



class PostUpdateView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Posts.objects.get(id=post_id)
        form = PostCreateForm(instance=post)
        context = {
            'post': post,
            'form': form
        }
        return render(request, 'crud/update_post.html', context)

    def post(self, request, post_id):
        post = Posts.objects.get(id=post_id)
        form = PostCreateForm(instance=post, data=request.POST)

        context = {
            'post': post,
            'form': form
        }

        if form.is_valid():
            form.save()
            return redirect(reverse('post_detail', kwargs={'id': post.id}))

        return render(request, 'crud/update_post.html', context)



class PostDeleteView(DeleteView):
    model = Posts
    template_name = 'crud/post_delete.html'
    success_url = reverse_lazy('my_posts')
    context_object_name = 'post'




class MyPostsView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Posts.objects.filter(author=self.request.user)
        page_obj = pagination(request, posts)
        return render(request, 'blog/my_posts.html', {'page_obj': page_obj})



class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, id):
        form = CommentForm(data=request.POST)
        post = Posts.objects.get(id=id)


        if form.is_valid():
            Comment.objects.create(
                posts=post,
                user=request.user,
                body=form.cleaned_data['body']
            )
            return redirect(reverse('post_detail', kwargs={'id': id}))
        return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


class SearchResultsList(ListView):
    model = Posts
    template_name = 'blog/search_result.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Posts.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )



class TaggedResults(View):
    def get(self,request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Posts.objects.filter(tags=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'blog/tagged_results.html', context)
