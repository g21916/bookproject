from django.shortcuts import render,redirect
from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView
from  .models import BookData
from django.views import View
from collections import defaultdict
from django.http import HttpResponse
from django.db import models  # 追加
from django.contrib import messages  # メッセージを追加




def index_view(request):
    object_list = BookData.objects.all()
    return render(request, 'book/index.html', {'object_list': object_list})

class GenreBookView(TemplateView):
    template_name='book/genre.html'

class ListBookView(ListView):
    template_name = 'book/book_list.html'
    model = BookData

    def get_queryset(self):
        # セッションからフィルタされた本のIDを取得
        filtered_book_ids = self.request.session.get('filtered_books', [])
        
        # IDに基づいて本のクエリセットを返す
        return BookData.objects.filter(id__in=filtered_book_ids)

class DetailBookView(DetailView):
    template_name = 'book/book_detail.html'
    model = BookData

def zero_view(request):
    return render(request, 'book/zero.html')  # ゼロ件のときのテンプレートを指定

class SelectThumbnailView(ListView):  # フィルターされた後のデータの表紙画像を一覧表示する
    template_name = 'book/select_thumbnail.html'  # 使用するテンプレート
    context_object_name = 'object_list'  # テンプレートに渡すオブジェクト名

    def get(self, request):
        # セッションからフィルタされた本を取得
        filtered_books = request.session.get('filtered_books', [])
        if not filtered_books:
            # フィルタ結果が空の場合はリダイレクトやエラーハンドリングを追加する
            return redirect('zero')  # 例えばzero.htmlにリダイレクト
        return render(request, self.template_name, {'object_list': BookData.objects.filter(id__in=filtered_books)})
    
class ProcessSelectedBooksView(View):
    # 書籍画像一覧で5つ選んだデータをセッションに保存してbook_list.htmlに返す
    def post(self, request):
        # 以前のセッションデータをクリア
        if 'filtered_books' in request.session:
            del request.session['filtered_books']

        # 選択された本のIDリストを取得
        selected_books = request.POST.getlist('selected_books')  # ここはselect_thumbnail.htmlのフォームから送信される名前に合わせてください

        # セッションに保存
        request.session['filtered_books'] = selected_books  

        print("Selected Books:", selected_books)  # デバッグ用の出力

        return redirect('list-book')  # 適切なリダイレクト先へ


def search_books_genre(request):
    genre = request.GET.get('genre')  # URLからgenreパラメータを取得
    books = BookData.objects.filter(Q(genre1=genre) | Q(genre2=genre))  # genre1かgenre2に一致するデータをフィルタリング
    request.session['search_results_genre'] = [book.id for book in books]  # 書籍IDだけをセッションに保存
    return render(request, 'book/search_results_genre.html', {'books': books, 'genre': genre})


def filter_books_by_story_type(request):
    story_type = request.GET.get('story_type')  # 短編/長編の選択を取得
    book_ids = request.session.get('search_results_genre', [])  # セッションからジャンル結果のIDを取得

    # IDのリストを使って本をフィルタリング
    if story_type == 'short':
        filtered_books = BookData.objects.filter(id__in=book_ids, short_story='短編')
    else:
        filtered_books = BookData.objects.filter(id__in=book_ids, short_story='')  # 長編のフィルタリング

    # 結果をセッションに保存
    request.session['filtered_books'] = [book.id for book in filtered_books]

    # 結果に応じてリダイレクトまたはテンプレートを返す
    if not filtered_books:
          return redirect('zero')  # 結果が0件の場合はzero.htmlにリダイレクト
 
    if story_type == 'short':
        if len(filtered_books) >= 6:
            # 受賞年を取得
            year_awarded = [book.year_awarded for book in filtered_books if book.year_awarded]
            # 受賞年が文字列の場合に整数に変換
            year_awarded = [int(year) for year in year_awarded if year.isdigit()]

            # 5年区切りで受賞年をグループ化
            year_ranges = defaultdict(list)
            for year in year_awarded:
                range_start = (year // 5) * 5  # 5年区切りの開始年
                range_end = range_start + 4  # 5年区切りの終了年
                year_ranges[f'{range_start}-{range_end}'].append(year)

            # テンプレートにフィルタ結果と年範囲を渡す
            return render(request, 'book/search_awards.html', {
                'object_list': filtered_books,
                'year_ranges': {k: v for k, v in year_ranges.items() if v},  # 書籍がある範囲のみ表示
            })
        else:
            return render(request, 'book/book_list.html', {'object_list': filtered_books})  # 1から5冊はbook_list.htmlに表示

    else:  # 長編の選択
        if 6 <= len(filtered_books) <= 13:
            return redirect('select_thumbnail')  # 6～13冊はSelectThumbnailViewにリダイレクト
        elif len(filtered_books) >= 14:
        # セッションに書籍データを保存
            request.session['filtered_books'] = list(filtered_books.values())

            return render(request, 'book/search_pages.html', {
                    'page_ranges': categorize_by_page(filtered_books),
                    'object_list': filtered_books,  # フィルタされた書籍のリストも渡す
                })
        else:
            return render(request, 'book/book_list.html', {'object_list': filtered_books})  # 1から5冊はbook_list.htmlに表示
        


def categorize_by_page(filtered_books):
    page_ranges = {}
    for book in filtered_books:
        try:
            page = int(book.page)
        except (ValueError, TypeError):
            continue
        
        start_page = (page // 50) * 50 + 1
        end_page = (page // 50 + 1) * 50
        
        range_key = f"{start_page} - {end_page}"
        
        if range_key not in page_ranges:
            page_ranges[range_key] = []
        page_ranges[range_key].append(book)

    # 書籍が存在するページ範囲のみ返す
    # さらに、キー（ページ範囲）をソートして返す
    sorted_page_ranges = dict(sorted(page_ranges.items(), key=lambda x: int(x[0].split(' - ')[0])))
    
    return sorted_page_ranges




        

def filter_by_year_range(request):
    # セッションからフィルタリング結果を取得（全体の結果を取得）
    filtered_ids = request.session.get('filtered_books', [])
    
    # 年範囲を取得
    year_range = request.GET.get('year_range')
    if year_range:
        start_year, end_year = map(int, year_range.split('-'))
        
        # フィルタリングされた書籍を取得
        books = BookData.objects.filter(id__in=filtered_ids, year_awarded__gte=start_year, year_awarded__lte=end_year)
        
        # フィルタリング結果をセッションに保存
        request.session['filtered_books_by_year'] = list(books.values_list('id', flat=True))
    
    # 書籍一覧を表示するためのテンプレートをレンダリング
    return render(request, 'book/book_list.html', {'object_list': books})




def filter_by_page_range(request, start_page, end_page):
    
    # 選択されたページ範囲のデータを保存
    # セッションから書籍のIDリストを取得
    filtered_books = request.session.get('filtered_books', [])

    # セッションに辞書形式ではなくIDのみ保存されているか確認
    if isinstance(filtered_books, list) and len(filtered_books) > 0 and isinstance(filtered_books[0], dict):
        # 辞書のリストが保存されている場合は、IDだけを取り出す
        filtered_books = [book['id'] for book in filtered_books]
        request.session['filtered_books'] = filtered_books  # IDリストをセッションに上書き保存

    # 書籍IDリストを使って、ページ範囲でフィルタ
    filtered_books_queryset = BookData.objects.filter(
        id__in=filtered_books, 
        page__gte=start_page, 
        page__lte=end_page
    )

    # フィルタ結果のIDリストをセッションに保存
    request.session['filtered_books'] = list(filtered_books_queryset.values_list('id', flat=True))
    
    # セッションデータの確認
    print(f"フィルタされた書籍のID: {request.session.get('filtered_books', 'セッションにデータがありません')}")
    print(f"フィルタ条件: {start_page}ページから{end_page}ページ")
    print(f"フィルタ結果の書籍数: {filtered_books_queryset.count()}")

    # フィルタされた書籍の情報を確認
    if filtered_books_queryset.exists():
        print(f"フィルタされた書籍のデータ: {[book.id for book in filtered_books_queryset]}")

    # page_rangesを初期化
    page_ranges = []

    # フィルタされた本の数に応じてレンダリング先を決定
    filtered_count = filtered_books_queryset.count()
    if 1 <= filtered_count <= 5:
        return render(request, 'book/book_list.html', {'object_list': filtered_books_queryset})
    elif filtered_count >= 6:
        page_ranges = categorize_by_page(filtered_books_queryset)
        #return render(request, 'book/search_pages.html', {'object_list': filtered_books_queryset, 'page_ranges': page_ranges})
        return redirect('select_thumbnail')
    else:
        return render(request, 'book/search_pages.html', {'page_ranges': page_ranges})  # 空のリストでも送信