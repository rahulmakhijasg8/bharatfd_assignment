from django.contrib import admin
from .models import FAQ
import asyncio
from .utils import trans
from django.core.cache import cache
from django.utils.html import strip_tags
import html


class FAQAdmin(admin.ModelAdmin):
    async def translate_all(self, question, answer):
        return await asyncio.gather(
            trans(question, 'Hindi'),
            trans(answer, 'Hindi'),
            trans(question, 'Bengali'),
            trans(answer, 'Bengali')
        )

    def save_model(self, request, obj, form, change):
        clean_answer = strip_tags(html.unescape(obj.answer))
        # translations = asyncio.run(self.translate_all(clean_question,
        # clean_answer))
        # # Update the instance with translated values
        obj.answer = clean_answer
        print(obj.question, obj.answer)
        # obj.question_hi = translations[0]
        # obj.answer_hi = translations[1]
        # obj.question_bn = translations[2]
        # obj.answer_bn = translations[3]
        cache.clear()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        cache.clear()
        super().delete_model(request, obj)


admin.site.register(FAQ, FAQAdmin)
