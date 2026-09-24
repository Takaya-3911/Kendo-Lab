from django.test import TestCase
from django.urls import reverse

from .models import Comment, KendoLevel, Post


class MainViewTests(TestCase):
    """メイン画面の見た目変更で既存の挙動が壊れていないことを確認する"""

    def setUp(self):
        self.suburi = Post.objects.create(
            post_type="video",
            category="正面素振り",
            experience_period="半年",
            title="素振りの投稿",
            nickname="はやて",
            memo="左手の位置を見てください",
        )
        self.kamae = Post.objects.create(
            post_type="image",
            category="中段の構え",
            experience_period="1ヶ月",
            title="構えの投稿",
            nickname="さくら",
        )
        Comment.objects.create(
            post=self.suburi,
            comment="刃筋が通っています",
            nickname="先生",
            level=KendoLevel.INSTRUCTOR,
        )

    def get_main(self, **params):
        return self.client.get(reverse("main"), params)

    def test_renders_with_new_design_assets(self):
        res = self.get_main()
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "kendo/main.html")
        self.assertContains(res, "kendo/css/style.css")
        self.assertContains(res, 'class="site-header"')
        self.assertContains(res, 'class="site-footer"')

    def test_latest_post_is_selected_by_default(self):
        res = self.get_main()
        self.assertEqual(res.context["selected_post"], self.kamae)
        self.assertContains(res, "構えの投稿")
        self.assertContains(res, "素振りの投稿")

    def test_selected_id_shows_that_post_with_memo_and_comments(self):
        res = self.get_main(selected_id=self.suburi.id)
        self.assertEqual(res.context["selected_post"], self.suburi)
        self.assertContains(res, "左手の位置を見てください")
        self.assertContains(res, "刃筋が通っています")
        self.assertContains(res, "指導員・先生")
        self.assertContains(res, 'data-level="instructor"')

    def test_category_filter_links_and_filtering(self):
        res = self.get_main(category="中段の構え")
        self.assertEqual(list(res.context["posts"]), [self.kamae])
        self.assertContains(res, "?category=%E4%B8%AD%E6%AE%B5%E3%81%AE%E6%A7%8B%E3%81%88")
        self.assertContains(res, "sb-link active")

    def test_sidebar_marks_selected_post_as_active(self):
        res = self.get_main(selected_id=self.suburi.id)
        self.assertContains(res, f"selected_id={self.suburi.id}")
        self.assertContains(res, 'aria-current="true"')

    def test_comment_form_keeps_api_contract(self):
        res = self.get_main(selected_id=self.suburi.id)
        self.assertContains(res, 'id="commentForm"')
        self.assertContains(res, f'name="post" value="{self.suburi.id}"')
        self.assertContains(res, 'name="nickname"')
        self.assertContains(res, 'name="level"')
        self.assertContains(res, 'name="comment"')
        self.assertContains(res, "/api/comments/")

    def test_create_post_modal_is_available(self):
        res = self.get_main()
        self.assertContains(res, 'id="openCreateModalBtn"')
        self.assertContains(res, 'id="createModal"')
        self.assertContains(res, "/api/register/")

    def test_empty_state_when_no_posts(self):
        Post.objects.all().delete()
        res = self.get_main()
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "表示できる投稿がありません")
        self.assertContains(res, "該当する投稿がありません")
