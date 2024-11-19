from django.contrib import admin
from django.utils.html import mark_safe  # 追加
# Register your models here.
from .models import BookData  # 追加
from import_export import resources  # 追加
from import_export.admin import ImportExportModelAdmin  # 追加
from import_export.fields import Field # 追加

class BookDataResource(resources.ModelResource):
   # field名とcsvの列名が異なる場合はここで指定する。
   # ここでは、postalcode / postalCode、category / categoriesと微妙に異なる。
   cust_id = Field(attribute='cust_id', column_name='ID')   
   award_winning = Field(attribute='award_winning', column_name='受賞回')
   title = Field(attribute='title', column_name='タイトル')
   author = Field(attribute='author', column_name='著者')
   publisher= Field(attribute='publisher', column_name='出版社')
   release_date = Field(attribute='release_date', column_name='発売日')
   isbn = Field(attribute='isbn', column_name='ISBN')
   page = Field(attribute='page', column_name='ページ数')
   summary = Field(attribute='summary', column_name='あらすじ')
   url = Field(attribute='url', column_name='AmazonURL')
   genre1 = Field(attribute='genre1', column_name='ジャンル1')
   genre2= Field(attribute='genre2', column_name='ジャンル2')
   short_story = Field(attribute='short_story', column_name='短編集か')
   year_awarded = Field(attribute='year_awarded', column_name='受賞年')
   # django-import-exportのModel設定
   class Meta:
       model = BookData
       # Controls if the import should skip unchanged records. Default value is False
       skip_unchanged = True
       use_bulk = True

@admin.register(BookData)
# ImportExportModelAdminを継承したAdminクラスを作成する
class BookDataAdmin(ImportExportModelAdmin):
   ordering = ['id']
   list_display = ('id','cust_id', 'award_winning', 'title', 'author', 'publisher', 'release_date','isbn','page','summary','url','genre1','genre2','short_story','year_awarded','thumbnail_display')
   # resource_classにModelResourceを継承したクラス設定
   resource_class = BookDataResource
   
   def thumbnail_display(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" style="width: 75px; height: auto;" />')  # 小さい画像を表示
        return "No Image"
   thumbnail_display.short_description = 'Thumbnail'  # 列のヘッダーを設定