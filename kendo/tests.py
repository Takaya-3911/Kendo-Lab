from django.test import TestCase

from .models import Post, PostImage


class SidebarPreviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.video_post = Post.objects.create(
            post_type="video",
            video="videos/sidebar-preview.mp4",
            category="サイドバー",
            experience_period="1年",
            title="動画投稿",
            nickname="剣士",
        )
        cls.image_post = Post.objects.create(
            post_type="image",
            category="サイドバー",
            experience_period="2年",
            title="画像投稿",
            nickname="剣士",
        )
        PostImage.objects.create(
            post=cls.image_post,
            image="images/sidebar-preview.png",
        )
        cls.video_with_image_post = Post.objects.create(
            post_type="video",
            video="videos/sidebar-preview-with-image.mp4",
            category="サイドバー",
            experience_period="2年",
            title="動画とサムネイル",
            nickname="剣士",
        )
        PostImage.objects.create(
            post=cls.video_with_image_post,
            image="images/video-thumbnail.png",
        )
        cls.empty_video_post = Post.objects.create(
            post_type="video",
            video="",
            category="サイドバー",
            experience_period="3年",
            title="動画ファイルなし",
            nickname="剣士",
        )
        cls.empty_image_post = Post.objects.create(
            post_type="image",
            category="サイドバー",
            experience_period="4年",
            title="画像ファイルなし",
            nickname="剣士",
        )

    def test_video_without_image_uses_first_frame_preview(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="post-preview video-preview"')
        self.assertContains(response, 'preload="metadata"')
        self.assertContains(
            response,
            'src="/media/videos/sidebar-preview.mp4#t=0.001"',
        )
        self.assertContains(
            response,
            'onloadedmetadata="this.currentTime = 0.001;"',
        )
        self.assertNotContains(response, 'src=""')

    def test_image_post_uses_first_related_image(self):
        response = self.client.get("/")

        self.assertContains(response, 'src="/media/images/sidebar-preview.png"')

    def test_video_with_related_image_uses_thumbnail(self):
        response = self.client.get("/")

        self.assertContains(response, 'src="/media/images/video-thumbnail.png"')
        self.assertContains(response, 'alt="動画とサムネイルのサムネイル"')

    def test_posts_without_media_use_default_placeholder(self):
        response = self.client.get("/")

        self.assertContains(
            response,
            'class="post-preview preview-placeholder"',
            count=2,
        )


class MainContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.video_and_image_post = Post.objects.create(
            post_type="video",
            video="videos/main-content.mp4",
            category="メイン",
            experience_period="1年",
            title="動画と画像",
            nickname="剣士",
            memo="動画と画像のメモ",
        )
        PostImage.objects.create(
            post=cls.video_and_image_post,
            image="images/main-content.png",
        )
        cls.video_without_memo_post = Post.objects.create(
            post_type="video",
            video="videos/main-content-no-memo.mp4",
            category="メイン",
            experience_period="2年",
            title="メモなし動画",
            nickname="剣士",
        )

    def test_video_image_and_memo_render_independently(self):
        response = self.client.get(
            f"/?selected_id={self.video_and_image_post.id}"
        )

        self.assertContains(
            response,
            'src="/media/videos/main-content.mp4"',
        )
        self.assertContains(
            response,
            'src="/media/images/main-content.png"',
        )
        self.assertContains(
            response,
            "<strong>稽古メモ:</strong> 動画と画像のメモ",
        )

    def test_memo_box_is_rendered_when_memo_is_empty(self):
        response = self.client.get(
            f"/?selected_id={self.video_without_memo_post.id}"
        )

        self.assertContains(
            response,
            'src="/media/videos/main-content-no-memo.mp4"',
        )
        self.assertContains(response, '<div class="memo-box">')
        self.assertContains(response, '<strong>稽古メモ:</strong>')
