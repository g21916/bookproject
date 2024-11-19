#class BookData(models.Model):
#    title = models.CharField(max_length=100)  #データの種類 titleがデータを呼び出す名前
#    number = models.IntegerField()
from django.db import models

class BookData(models.Model):
   id = models.AutoField(primary_key=True)
   cust_id = models.CharField(verbose_name='ID', max_length=100, blank=True, null=True)
   award_winning = models.CharField(verbose_name='受賞回', max_length=100, blank=True, null=True)
   title = models.CharField(verbose_name='タイトル', max_length=100, blank=True, null=True)
   author = models.CharField(verbose_name='著者', max_length=100, blank=True, null=True)
   publisher = models.CharField(verbose_name='出版社', max_length=100, blank=True, null=True)
   release_date = models.CharField(verbose_name='発売日', max_length=100, blank=True, null=True)
   isbn = models.CharField(verbose_name='ISBN', max_length=20, blank=True, null=True)
   page = models.IntegerField(verbose_name='ページ数',  blank=True, null=True)
   summary = models.TextField(verbose_name='あらすじ', blank=True, null=True)
   url = models.TextField(verbose_name='AmazonURL',blank=True, null=True)
   genre1 = models.CharField(verbose_name='ジャンル1', max_length=100, blank=True, null=True)
   genre2 = models.CharField(verbose_name='ジャンル2', max_length=100, blank=True, null=True)
   short_story = models.CharField(verbose_name='短編集か', max_length=100, blank=True, null=True)
   year_awarded = models.CharField(verbose_name='受賞年', max_length=100, blank=True, null=True)
   thumbnail= models.ImageField(upload_to='book_thumbnails/', null=True, blank=True)

   def __str__(self):
        return self.title
   

class Meta:
       db_table = 'book_data'
       verbose_name = '直木賞の書籍'
       verbose_name_plural = '直木賞書籍リスト'