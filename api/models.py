from django.db import models
from ckeditor.fields import RichTextField


class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    question_hi = models.CharField(null=True, blank=True, max_length=255)
    answer_hi = models.CharField(null=True, blank=True, max_length=255)
    question_bn = models.CharField(null=True, blank=True, max_length=255)
    answer_bn = models.CharField(null=True, blank=True, max_length=255)

    def get_translated_question(self, lang):
        return getattr(self, f'question_{lang}', self.question)

    def get_translated_answer(self, lang):
        return getattr(self, f'answer_{lang}', self.answer)
