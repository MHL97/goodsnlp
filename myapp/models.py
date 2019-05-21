from django.db import models


# Create your models here.

class Platform(models.Model):
    platform = models.CharField(max_length=20)
    result_path = models.CharField(max_length=255)


class Sorts(models.Model):
    sorts_name = models.CharField(max_length=20)
    result_path = models.CharField(max_length=255)


class Base(models.Model):
    product_id = models.CharField(max_length=20)
    product_url = models.CharField(max_length=255, primary_key=True)
    product_title = models.CharField(max_length=255)
    img_url = models.CharField(max_length=255)
    good_rote = models.FloatField(max_length=5)
    good_num = models.CharField(max_length=10)
    mid_num = models.CharField(max_length=10)
    poor_num = models.CharField(max_length=10)
    total_num = models.CharField(max_length=10)
    sorts_id = models.IntegerField()
    platform_id = models.IntegerField()


class Analysis(models.Model):
    product_id = models.CharField(max_length=20)
    product_url = models.CharField(max_length=255, primary_key=True)
    good_rote = models.FloatField(max_length=5)
    poor_rote = models.FloatField(max_length=5)
    good_num = models.IntegerField()
    mid_num = models.IntegerField()
    poor_num = models.IntegerField()
    total_num = models.IntegerField()

    all_cloud = models.CharField(max_length=255)
    poor_cloud = models.CharField(max_length=255)
    good_cloud = models.CharField(max_length=255)

    # all_freq_h = models.CharField(max_length=255)
    # good_freq_h = models.CharField(max_length=255)
    # poor_freq_h = models.CharField(max_length=255)

    all_sent_h = models.CharField(max_length=255)
    good_sent_h = models.CharField(max_length=255)
    mid_sent_h = models.CharField(max_length=255)
    poor_sent_h = models.CharField(max_length=255)

    top_all_freq = models.CharField(max_length=255)
    top_good_freq = models.CharField(max_length=255)
    top_poor_freq = models.CharField(max_length=255)


class Comments(models.Model):
    product_id = models.CharField(max_length=20)
    product_url = models.CharField(max_length=255)
    old_text = models.CharField(max_length=255)
    new_text = models.CharField(max_length=255)
    sent_score = models.FloatField(max_length=10)
    key_words = models.CharField(max_length=255)
    is_post = models.CharField(max_length=2)
