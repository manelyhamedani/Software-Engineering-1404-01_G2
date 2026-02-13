import logging

from celery import shared_task
from django.conf import settings
from team2.models import Version, Article

INDEX_NAME = "articles"
_ES = None


def _get_es():
    global _ES
    if _ES is None:
        from elasticsearch import Elasticsearch
        _ES = Elasticsearch(hosts=[settings.ELASTICSEARCH_URL])
    return _ES


@shared_task(bind=True, max_retries=2, default_retry_delay=10)
def index_article_version(self, results, version_name):
    version = Version.objects.get(name=version_name)
    body = {
        "article_name": version.article.name,
        "version_name": version.name,
        "content": version.content,
        "summary": version.summary,
        "tags": [tag.name for tag in version.tags.all()],
        "article_score": version.article.score,
        "article_created_at": version.article.created_at.isoformat(),
    }

    try:
        _get_es().index(index=INDEX_NAME, id=version.name, document=body)
    except Exception as exc:
        raise self.retry(exc=exc)


def search_articles_semantic(query, size=10):
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content", "summary^2", "tags^3"],
                "fuzziness": "AUTO"
            }
        },
        "size": size
    }

    resp = _get_es().search(index=INDEX_NAME, body=search_body)
    results = []

    for hit in resp["hits"]["hits"]:
        results.append({
            "article_name": hit["_source"]["article_name"],
            "version_name": hit["_source"]["version_name"],
            "score": hit["_score"],
            "summary": hit["_source"]["summary"],
            "tags": hit["_source"]["tags"],
        })

    return results

def map_es_to_articles(es_hits):
    names = [hit["_source"]["article_name"] for hit in es_hits]

    articles = {
        a.name: a
        for a in Article.objects.filter(name__in=names)
        .select_related("current_version")
    }

    result = []
    for hit in es_hits:
        name = hit["_source"]["article_name"]
        article = articles.get(name)
        if not article:
            continue
        result.append(article)

    return result

def find_top_articles(limit):
    body = {
        "query": {"match_all": {}},
        "size": limit,
        "sort": [
            {"article_score": {"order": "desc"}}
        ]
    }

    resp = _get_es().search(index=INDEX_NAME, body=body)

    articles = map_es_to_articles(resp["hits"]["hits"])

    return articles

def find_recent_articles(limit):
    body = {
        "query": {"match_all": {}},
        "size": limit,
        "sort": [
            {"created_at": {"order": "desc"}}
        ]
    }

    resp = _get_es().search(index=INDEX_NAME, body=body)

    articles = map_es_to_articles(resp["hits"]["hits"])

    return articles