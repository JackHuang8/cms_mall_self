from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import News, NewsCategory
from news.serializers import NewsSerializer, NewsCategorySerializer


class NewsTopView(APIView):
    def get(self,request):
        slides_obj = News.objects.filter(is_slide=1)
        recommend_obj = News.objects.order_by('-create_time')[0:10]
        picture_obj = News.objects.exclude(img_url='').order_by('-click')[0:4]

        slides_data = NewsSerializer(slides_obj, many=True).data
        recommend_data = NewsSerializer(recommend_obj, many=True).data
        picture_news = NewsSerializer(picture_obj, many=True).data

        data = {
            'slides_data':slides_data,
            'recommend_data':recommend_data,
            'picture_news':picture_news,
        }

        return Response(data)


class NewsCategoryView(APIView):
    def get(self, request):
        data = []
        b_category_obj = NewsCategory.objects.filter(parent_id=0)
        for b_obj in b_category_obj:
            dict = {}
            dict['title'] = b_obj.title
            s_queryset = NewsCategory.objects.filter(parent=b_obj)
            dict['newscategory_set'] = NewsCategorySerializer(s_queryset, many=True).data

            news_queryset = News.objects.filter(category__in=s_queryset).order_by('-create_time')[0:4]
            dict['news'] = NewsSerializer(news_queryset, many=True).data

            top8_queryset = News.objects.filter(category__in=s_queryset).order_by('-click')[0:8]
            dict['top8'] = NewsSerializer(top8_queryset, many=True).data

            data.append(dict)
        return Response(data)
