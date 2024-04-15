from django.urls import path

from posts.views import HomePageView, AboutPageView, ContactPageView, LatestPostsView, CPlusView, PythonView, PHPView, \
    JavaScriptView, CSSView, ProgrammingView, HostingView, OtherInformView, PostDetailView, AddCommentView, \
    PostUpdateView, PostDeleteView, PostCreateView, MyPostsView, SearchResultsList, TaggedResults

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home_page'),
    path('about/', AboutPageView.as_view(), name='about_page'),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('features', LatestPostsView.as_view(), name='latest_posts'),
    path('C++/', CPlusView.as_view(), name='c++'),
    path('python/', PythonView.as_view(), name='python'),
    path('PHP/', PHPView.as_view(), name='php'),
    path('javascript/', JavaScriptView.as_view(), name='javascript'),
    path('CSS/', CSSView.as_view(), name='css'),
    path('learning_programming/', ProgrammingView.as_view(), name='learning_programming'),
    path('hosting/', HostingView.as_view(), name='hosting'),
    path('another/', OtherInformView.as_view(), name='another'),
    path('<int:id>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:id>/comments', AddCommentView.as_view(), name='comments'),
    path('<int:post_id>/edit/', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('my_posts/', MyPostsView.as_view(), name='my_posts'),
    path('search-results/', SearchResultsList.as_view(), name='search_result'),
    path('tagged/<slug:slug>/', TaggedResults.as_view(), name='tagged')
]
