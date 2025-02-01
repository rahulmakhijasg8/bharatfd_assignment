import pytest
from api.models import FAQ
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def faq_instance():
    """Fixture to create a sample FAQ instance."""
    return FAQ.objects.create(
        question="What is Django?",
        answer="Django is a web framework.",
        question_hi="डिजैंगो क्या है?",
        answer_hi="डिजैंगो एक वेब फ्रेमवर्क है।",
        question_bn="ডিজ্যাঙ্গো কী?",
        answer_bn="ডিজ্যাঙ্গো একটি ওয়েব ফ্রেমওয়ার্ক।"
    )


@pytest.mark.django_db
def test_get_translated_question(faq_instance):
    assert faq_instance.get_translated_question('en') == "What is Django?"
    assert faq_instance.get_translated_question('hi') == "डिजैंगो क्या है?"
    assert faq_instance.get_translated_question('bn') == "ডিজ্যাঙ্গো কী?"
    assert faq_instance.get_translated_question('fr') == "What is Django?"


@pytest.mark.django_db
def test_get_translated_answer(faq_instance):
    assert all([faq_instance.get_translated_answer('en')
               == "Django is a web framework.",
               faq_instance.get_translated_answer('hi') ==
               "डिजैंगो एक वेब फ्रेमवर्क है।",
                faq_instance.get_translated_answer('bn') ==
                "ডিজ্যাঙ্গো একটি ওয়েব ফ্রেমওয়ার্ক।",
                faq_instance.get_translated_answer('fr') ==
                "Django is a web framework."])


@pytest.mark.django_db
def test_faq_creation(faq_instance):
    assert faq_instance.question == "What is Django?"
    assert faq_instance.answer == "Django is a web framework."
    assert faq_instance.question_hi == "डिजैंगो क्या है?"
    assert faq_instance.answer_hi == "डिजैंगो एक वेब फ्रेमवर्क है।"
    assert faq_instance.question_bn == "ডিজ্যাঙ্গো কী?"
    assert faq_instance.answer_bn == "ডিজ্যাঙ্গো একটি ওয়েব ফ্রেমওয়ার্ক।"


@pytest.mark.django_db
def test_get_translated_question_default(faq_instance):
    assert faq_instance.get_translated_question('es') == faq_instance.question


@pytest.mark.django_db
def test_get_translated_answer_default(faq_instance):
    assert faq_instance.get_translated_answer('es') == faq_instance.answer


@pytest.fixture
def valid_data():
    return {
        'question': 'What is Python?',
        'answer': 'Python is a programming language.'
    }


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_faq(api_client, valid_data):
    url = '/api/faqs/'
    response = api_client.post(url, valid_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['question'] == valid_data['question']
    assert response.data['answer'] == valid_data['answer']


@pytest.mark.django_db
def test_list_faq(api_client, faq_instance):
    url = '/api/faqs/'
    response = api_client.get(url, {'lang': 'en'}, format='json')
    cached_data = cache.get('faq_hi')
    assert cached_data is None
    api_client.get(url, {'lang': 'hi'}, format='json')
    cached_data = cache.get('faq_hi')
    response_cached = api_client.get(url, {'lang': 'hi'}, format='json')
    assert cached_data is not None
    assert response_cached.data == cached_data
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['question'] == faq_instance.question
    assert response.data[0]['answer'] == faq_instance.answer


@pytest.mark.django_db
def test_retrieve_faq(api_client, faq_instance):
    url = f'/api/faqs/{faq_instance.id}/'
    response = api_client.get(url, {'lang': 'en'}, format='json')
    cached_value = cache.get(f'faq_{faq_instance.id}_hi')
    api_client.get(url, {'lang': 'hi'}, format='json')
    cached_value = cache.get(f'faq_{faq_instance.id}_hi')
    assert cached_value is not None
    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == faq_instance.question
    assert response.data['answer'] == faq_instance.answer


@pytest.mark.django_db
def test_retrieve_faq_with_translation(api_client, faq_instance):
    url = f'/api/faqs/{faq_instance.id}/'
    response = api_client.get(url, {'lang': 'hi'}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == faq_instance.question_hi
    assert response.data['answer'] == faq_instance.answer_hi


@pytest.mark.django_db
def test_retrieve_faq_cache(api_client, faq_instance):
    url = f'/api/faqs/{faq_instance.id}/'
    api_client.get(url, {'lang': 'hi'}, format='json')
    cached_value = cache.get(f'faq_{faq_instance.id}_hi')
    assert cached_value is not None


@pytest.mark.django_db
def test_update_faq(api_client, faq_instance):
    url = f'/api/faqs/{faq_instance.id}/'
    updated_data = {
        'question': 'What is Django Framework?',
        'answer': 'Django is a high-level Python web framework.'
    }
    response = api_client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == updated_data['question']
    assert response.data['answer'] == updated_data['answer']


@pytest.mark.django_db
def test_delete_faq(api_client, faq_instance):
    url = f'/api/faqs/{faq_instance.id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert FAQ.objects.count() == 0


@pytest.mark.django_db
def test_cache_clear_after_update(api_client, faq_instance):
    url = f'/api/faqs/{faq_instance.id}/'
    updated_data = {
        'question': 'Updated Question?',
        'answer': 'Updated Answer!'
    }
    api_client.put(url, updated_data, format='json')
    assert cache.get(f'faq_{faq_instance.id}_en') is None


@pytest.mark.django_db
def test_cache_clear_after_delete(api_client, faq_instance):
    url = f'/api/faqs/{faq_instance.id}/'
    api_client.delete(url)
    assert cache.get(f'faq_{faq_instance.id}_en') is None
