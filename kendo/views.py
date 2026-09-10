from django.shortcuts import render

def video_sidebar_view(request):
    # 稽古種目フィルターのリスト
    filters = ['すべて', '正面素振り', '中段の構え', '跳躍素振り（早素振り）', '左右素振り', '胴打ち・その他']

    # 他の剣士の稽古動画・画像データ（仮のデータ）
    dummy_videos = [
        {
            'id': 1,
            'title': '【動画】跳躍素振り50本！息が上がると竹刀がブレてしまいます',
            'user_name': 'はやて',
            'user_role': '初心者 (半年)',
            'score': 78,
            'type': '動画',
        },
        {
            'id': 2,
            'title': '【写真3枚】中段の構え（正面・側面・足元）のチェックをお願いします',
            'user_name': 'さくら剣士',
            'user_role': '初心者 (1ヶ月)',
            'score': 89,
            'type': '3枚',
        },
        {
            'id': 3,
            'title': '【初心者】正面素振り100本チャレンジ！刃筋と左手の位置を見てください',
            'user_name': '剣道はじめたて太郎',
            'user_role': '初心者 (2ヶ月)',
            'score': 84,
            'type': '動画',
        },
    ]

    context = {
        'filters': filters,
        'dummy_videos': dummy_videos,
        'selected_filter': 'すべて',
    }

    return render(request, 'kendo/video_sidebar.html', context)