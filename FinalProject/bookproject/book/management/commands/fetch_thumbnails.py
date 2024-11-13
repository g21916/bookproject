import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from ...models import BookData
import time

class Command(BaseCommand):
    help = "Fetch book thumbnails from API based on ISBN"

    def handle(self, *args, **kwargs):
        books = BookData.objects.all()

        for book in books:
            if book.isbn:  # ISBNがある場合
                isbn = book.isbn.strip()  
                url_ndl = f"https://ndlsearch.ndl.go.jp/thumbnail/{isbn}.jpg"
                
                # NDLから画像を取得
                response = requests.get(url_ndl)

                if response.status_code == 200:
                    book.thumbnail.save(f'{isbn}.jpg', ContentFile(response.content))
                    self.stdout.write(self.style.SUCCESS(f'Successfully saved thumbnail for ISBN: {isbn}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Failed to fetch image from NDL for ISBN: {isbn}. Status code: {response.status_code}'))
                    self.stdout.write(self.style.WARNING(f'Response: {response.content}'))

                    # 代替のURLを使用して画像を取得
                    url_hanmoto = f"https://img.hanmoto.com/bd/img/{isbn}.jpg"
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                    }
                    response_hanmoto = requests.get(url_hanmoto, headers=headers)  # headersを追加

                    if response_hanmoto.status_code == 200:
                        book.thumbnail.save(f'{isbn}.jpg', ContentFile(response_hanmoto.content))
                        self.stdout.write(self.style.SUCCESS(f'Successfully saved thumbnail from Hanmoto for ISBN: {isbn}'))
                    elif response_hanmoto.status_code == 503:
                        self.stdout.write(self.style.WARNING(f'Service unavailable from Hanmoto for ISBN: {isbn}. Retrying...'))
                        time.sleep(5)  # 5秒待機して再試行
                        response_hanmoto = requests.get(url_hanmoto, headers=headers)  # 再試行時もheadersを追加
                        if response_hanmoto.status_code == 200:
                            book.thumbnail.save(f'{isbn}.jpg', ContentFile(response_hanmoto.content))
                            self.stdout.write(self.style.SUCCESS(f'Successfully saved thumbnail from Hanmoto for ISBN: {isbn} (after retry)'))
                        else:
                            self.stdout.write(self.style.WARNING(f'Failed to fetch image from Hanmoto for ISBN: {isbn}. Status code: {response_hanmoto.status_code}'))
                            self.stdout.write(self.style.WARNING(f'Response: {response_hanmoto.content}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Failed to fetch image from Hanmoto for ISBN: {isbn}. Status code: {response_hanmoto.status_code}'))
                        self.stdout.write(self.style.WARNING(f'Response: {response_hanmoto.content}'))
