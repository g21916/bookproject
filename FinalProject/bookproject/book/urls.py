from django.urls import path

from . import views
from django.conf import settings#この2行を追加した
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index_view, name = 'index'),
    path('book/genre/',views.GenreBookView.as_view(), name='genre'),
    path('book/', views.ListBookView.as_view() , name = 'list-book'), #book_list.htmlの操作
    path('book/<int:pk>/detail/',views.DetailBookView.as_view(), name = 'detail-book'),
    path('book/search_books_genre/', views.search_books_genre, name='search_books_genre'),  # 'search_books'に対応するURLパターン
    path('book/filter-story-type/', views.filter_books_by_story_type, name='filter_books_by_story_type'),
    path('zero/', views.zero_view, name='zero'),  #0件の時のURL
    path('book/search_awards/', views.ListBookView.as_view(template_name='book/search_awards.html'), name='search_awards'),
    path('book/select-thumbnail/', views.SelectThumbnailView.as_view(), name='select_thumbnail'),  # クラスベースビューの登録
    path('book/process-selected-books/', views.ProcessSelectedBooksView.as_view(), name='process-selected-books'),  # 書籍画像を5つ選んだ時
    path('filter_by_year_range/', views.filter_by_year_range, name='filter_by_year_range'),
    path('filter-by-page-range/<int:start_page>/<int:end_page>/', views.filter_by_page_range, name='filter_by_page_range'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)