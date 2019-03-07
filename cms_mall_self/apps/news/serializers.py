from rest_framework.serializers import ModelSerializer

from news.models import News, NewsCategory


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class NewsCategorySerializer(ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = "__all__"
