from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in DictReader(open('static/data/users.csv', encoding="utf8")):
            user = User(
                id=row['id'], username=row['username'], email=row['email'],
                first_name=row['first_name'], last_name=row['last_name'],
                bio=row['bio'], role=row['role']
            )
            user.save()
        for row in DictReader(open('static/data/category.csv',
                                   encoding="utf8")):
            category = Category(
                id=row['id'], name=row['name'],
                slug=row['slug']
            )
            category.save()
        for row in DictReader(open('static/data/genre.csv', encoding="utf8")):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()
        for row in DictReader(open('static/data/titles.csv', encoding="utf8")):
            title = Title(
                id=row['id'], name=row['name'], year=row['year'],
                category=Category.objects.get(pk=row['category'])
            )
            title.save()
        for row in DictReader(open('static/data/genre_title.csv',
                                   encoding="utf8")):
            genre_title = GenreTitle(
                id=row['id'],
                genre=Genre.objects.get(pk=row['genre_id']),
                title=Title.objects.get(pk=row['title_id'])
            )
            genre_title.save()
        for row in DictReader(open('static/data/review.csv',
                                   encoding="utf8")):
            review = Review(
                id=row['id'], text=row['text'],
                score=row['score'], pub_date=row['pub_date'],
                author=User.objects.get(pk=row['author']),
                title=Title.objects.get(pk=row['title_id'])
            )
            review.save()
        for row in DictReader(open('static/data/comments.csv',
                                   encoding="utf8")):
            comment = Comment(
                id=row['id'], text=row['text'],
                pub_date=row['pub_date'],
                author=User.objects.get(pk=row['author']),
                review=Review.objects.get(pk=row['review_id']),
            )
            comment.save()
