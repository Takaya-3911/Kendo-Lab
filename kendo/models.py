from django.db import models


class Post(models.Model):
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")
    category = models.CharField("カテゴリ", max_length=50)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "投稿"
        verbose_name_plural = "投稿"

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="投稿",
    )
    author = models.CharField("投稿者", max_length=100)
    body = models.TextField("コメント")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "コメント"
        verbose_name_plural = "コメント"

    def __str__(self):
        return f"{self.author}: {self.body[:20]}"


class AiAnalysis(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="analyses",
        verbose_name="投稿",
    )
    score = models.IntegerField("スコア", default=50)
    summary = models.TextField("分析結果")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "AI分析"
        verbose_name_plural = "AI分析"

    def __str__(self):
        return f"{self.post.title} ({self.score}点)"
