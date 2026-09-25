from django.test import TestCase
from django.urls import reverse

from .models import Comment, KendoLevel, Post


class MainRegressionTests(TestCase):
    """{Kendo} ブランチを取り込んでも、main の既存画面・API が変わらないことを確認する"""

    def setUp(self):
        self.post = Post.objects.create(
            post_type="video",
            category="正面素振り",
            experience_period="半年",
            title="素振りの投稿",
            nickname="はやて",
            memo="左手の位置を見てください",
        )
        Comment.objects.create(
            post=self.post,
            comment="刃筋が通っています",
            nickname="先生",
            level=KendoLevel.INSTRUCTOR,
        )

    def test_top_page_still_uses_main_template(self):
        res = self.client.get(reverse("main"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "kendo/main.html")
        self.assertContains(res, "素振りの投稿")
        self.assertContains(res, "刃筋が通っています")
        self.assertContains(res, 'id="openCreateModalBtn"')

    def test_registration_page_still_available(self):
        res = self.client.get(reverse("registration"))
        self.assertEqual(res.status_code, 200)

    def test_api_posts_and_comments_still_work(self):
        res = self.client.get("/api/posts/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()[0]["title"], "素振りの投稿")

        res = self.client.post(
            "/api/comments/",
            {"post": self.post.id, "nickname": "さくら", "comment": "参考になります", "level": "shodan"},
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["level_display"], "初段")
