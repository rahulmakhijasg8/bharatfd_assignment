from rest_framework import viewsets, status
from .models import FAQ
from .serializers import FAQserializer
from rest_framework.response import Response
from django.utils.html import strip_tags
from .utils import trans
import asyncio
from django.core.cache import cache


# lang_dict = {
#     'hi_question':'सवाल', 'hi_answer':'उत्तर',
#     'bn_question':'প্রশ্ন', 'bn_answer':'উত্তর'
# }


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQserializer

    async def translate_all(self, question, answer):
        return await asyncio.gather(
            trans(question, 'Hindi'),
            trans(answer, 'Hindi'),
            trans(question, 'Bengali'),
            trans(answer, 'Bengali')
        )

    def get_permissions(self):
        if self.request.GET.get('lang'):
            self.http_method_names = ['get']
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cache.clear()
        clean_question = strip_tags(serializer.validated_data['question'])
        clean_answer = strip_tags(serializer.validated_data['answer'])
        translations = asyncio.run(self.translate_all(clean_question,
                                   clean_answer))
        serializer.validated_data.update({
            'question': clean_question,
            'answer': clean_answer,
            'question_hi': translations[0],
            'answer_hi': translations[1],
            'question_bn': translations[2],
            'answer_bn': translations[3]
        })
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', None)
        cache_key = f'faq_{lang}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        if lang in ['hi', 'bn']:
            resp = [{'id': obj.id,
                    'question': obj.get_translated_question(lang),
                     'answer': obj.get_translated_answer(lang)}
                    for obj in FAQ.objects.all()]
            cache.set(f'faq_{lang}', resp, timeout=3600)
            return Response(resp, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        lang = request.GET.get('lang', 'en')
        cache_key = f'faq_{instance.id}_{lang}'
        cached_value = cache.get(cache_key)
        if cached_value:
            return Response(cached_value, status=status.HTTP_200_OK)
        if lang in ['hi', 'bn']:
            resp = {'id': instance.id,
                    'question': instance.get_translated_question(lang),
                    'answer': instance.get_translated_answer(lang)}
            cache.set(cache_key, resp, timeout=3600)
            return Response(resp, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        clean_question = strip_tags(serializer.validated_data['question'])
        clean_answer = strip_tags(serializer.validated_data['answer'])
        translations = asyncio.run(self.translate_all(clean_question,
                                   clean_answer))
        serializer.validated_data.update({
            'question': clean_question,
            'answer': clean_answer,
            'question_hi': translations[0],
            'answer_hi': translations[1],
            'question_bn': translations[2],
            'answer_bn': translations[3]
        })
        self.perform_update(serializer)
        cache.clear()
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.clear()
        return response
