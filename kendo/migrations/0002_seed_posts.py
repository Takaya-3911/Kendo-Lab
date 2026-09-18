from django.db import migrations


def seed_posts(apps, schema_editor):
    Post = apps.get_model("kendo", "Post")
    posts = [
        ("構えの基本：竹刀の握り方", "握りの強弱が軸のブレに直結します。左手は軽く握り、右手は添えるだけ。",
         "構え"),
        ("正しい中段の構えの作り方", "左足のつま先を相手方向に向け、腰の高さを一定に保つのがポイントです。",
         "構え"),
        ("すり足の正しい運び方", "かかとを浮かせず、つま先で地面をなめるように運ぶとブレを抑えられます。",
         "足さばき"),
        ("踏み込みのタイミングを掴む", "振りの頂点から踏み込むのではなく、足が着く瞬間に打つリズムを意識しましょう。",
         "足さばき"),
        ("面打ちの基本動作とは", "左手を支点にして竹刀を振り上げ、正中線に沿って振り下ろします。",
         "打突"),
        ("小手打ちで意識する体軸", "手を伸ばすのではなく、腰を落として体全体で攻め込むことが大切です。",
         "打突"),
        ("毎日の素振りメニュー", "朝晩5分の素振りでも、軸を意識するだけで効果が変わります。",
         "トレーニング"),
        ("柔軟性アップのストレッチ", "稽古前のストレッチで股関節をほぐすと、足さばきが軽くなります。",
         "トレーニング"),
    ]
    Post.objects.bulk_create(
        [Post(title=t, content=c, category=cat) for t, c, cat in posts]
    )


def unseed_posts(apps, schema_editor):
    Post = apps.get_model("kendo", "Post")
    Post.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("kendo", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_posts, unseed_posts),
    ]