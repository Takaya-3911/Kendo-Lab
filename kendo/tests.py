from django.test import TestCase
from django.urls import reverse

from .models import Comment, Post


class PostApiTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            post_type="video", experience_period="1年", nickname="投稿者",
            title="テスト投稿", memo="テスト本文", category="構え"
        )
        self.comment = Comment.objects.create(
            post=self.post, nickname="太郎", comment="良い記事ですね"
        )

    def test_home_renders_selected_post(self):
        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "テスト投稿")
        self.assertContains(res, "良い記事ですね")

    def test_posts_json_filters_by_category(self):
        Post.objects.create(
            post_type="video", experience_period="1年", nickname="投稿者",
            title="絞り込み確認", memo="x", category="テスト専用"
        )
        res = self.client.get(reverse("posts_json"), {"category": "テスト専用"})
        data = res.json()
        self.assertEqual([p["title"] for p in data["posts"]], ["絞り込み確認"])

    def test_post_detail_json_includes_analysis_and_comments(self):
        res = self.client.get(reverse("post_detail_json", args=[self.post.id]))
        data = res.json()
        self.assertEqual(data["post"]["title"], "テスト投稿")
        self.assertIsNone(data["analysis"])
        self.assertEqual(data["comments"][0]["body"], "良い記事ですね")

    def test_add_comment_creates_comment(self):
        res = self.client.post(
            reverse("add_comment", args=[self.post.id]),
            {"author": "花子", "body": "コメントです"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["ok"])
        self.assertEqual(Comment.objects.count(), 2)
        comment = self.post.comments.latest("id")
        self.assertEqual(comment.nickname, "花子")

    def test_add_comment_empty_body_rejected(self):
        res = self.client.post(
            reverse("add_comment", args=[self.post.id]), {"author": "", "body": "  "}
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(Comment.objects.count(), 1)