from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = 'category'
        managed = False


class Product(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    image = models.CharField(max_length=200)
    category = models.ForeignKey(Category, db_column='category_id', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'product'
        managed = False
