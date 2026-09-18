from django.db import migrations


def seed_analyses(apps, schema_editor):
    Post = apps.get_model("kendo", "Post")
    AiAnalysis = apps.get_model("kendo", "AiAnalysis")
    by_title = {p.title: p for p in Post.objects.all()}
    analyses = [
        ("構えの基本：竹刀の握り方", 78,
         "握りすぎで指先が固く、竹刀が上下にブレやすい傾向。左手の小指・薬指で支え、右手は添える意識で安定します。"),
        ("正しい中段の構えの作り方", 85,
         "体軸は概ね良好。左足のつま先がやや外を向き、踏み込み時の重心移動が滑らかでない箇所があります。腰の高さを一定に保ちましょう。"),
        ("すり足の正しい運び方", 82,
         "かかとの浮きが小さく良い傾向。ただし歩幅が狭く、間を詰める速度がやや遅め。つま先で地面をなめるイメージで大きく運ぶと改善します。"),
        ("踏み込みのタイミングを掴む", 72,
         "振り上げと足の着地のタイミングがずれ、打突音が小さくなっています。足が着く瞬間に打つリズムを意識して反復練習しましょう。"),
        ("面打ちの基本動作とは", 80,
         "振り下ろしで左手が弓なりに曲がり、竹刀の軌道が円弧になっています。正中線の延長線上に振り下ろすイメージで矯正しましょう。"),
    ]
    AiAnalysis.objects.bulk_create(
        [
            AiAnalysis(post=by_title[title], score=score, summary=summary)
            for title, score, summary in analyses
            if title in by_title
        ]
    )


def unseed_analyses(apps, schema_editor):
    AiAnalysis = apps.get_model("kendo", "AiAnalysis")
    AiAnalysis.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("kendo", "0003_aianalysis_comment"),
    ]

    operations = [
        migrations.RunPython(seed_analyses, unseed_analyses),
    ]