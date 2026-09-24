from django.db import models
class KendoLevel(models.TextChoices):
    BEGINNER = "beginner", "初心者"
    ONE_YEAR = "1_year", "剣道歴1年"
    SHODAN = "shodan", "初段"
    NIDAN = "nidan", "二段"
    SANDAN = "sandan", "三段"
    DAN_4_PLUS = "4th_dan_plus", "四段以上"
    INSTRUCTOR = "instructor", "指導員・先生"
    
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

# コメント
# on_delete=models.CASCADEは参照先のオブジェクトが削除されたらこのオブジェクトも削除
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # コメント
    comment = models.TextField()
    # ニックネーム
    nickname = models.CharField(max_length=100)
    # 投稿者の段位

    level = models.CharField(
        max_length=20,
        choices=KendoLevel.choices,
        default=KendoLevel.BEGINNER,
    )
    # タイムスタンプ（動画内の再生位置）
    video_time_seconds = models.PositiveIntegerField(
        null=True, blank=True
    )
    @property
    def video_time_display(self):
        if self.video_time_seconds is None:
            return None
        minutes, seconds = divmod(self.video_time_seconds, 60)
        return f"{minutes}:{seconds:02d}"
    # コメント投稿日時
    created_at = models.DateTimeField(auto_now_add=True)

    # Comment.objects.all()したときに自動的に個の並び順で取得できる
    class Meta:
        ordering = ["-created_at"]
    