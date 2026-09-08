from django.db import models

# 投稿データ
class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('video', '動画'),
        ('image', '画像'),
    ]

    # 投稿タイプ
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    # 動画
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    # 稽古種目
    category = models.CharField(max_length=100)
    # 経験期間
    experience_period = models.CharField(max_length=50)
    # 投稿タイトル
    title = models.CharField(max_length=200)
    # ニックネーム
    nickname = models.CharField(max_length=100)
    # 投稿メモ
    memo = models.TextField(blank=True)
    # 投稿日時
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 投稿画像
class PostImage(models.Model):
    # 投稿データの外部キー
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    # 画像
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.post.title} - {self.id}'