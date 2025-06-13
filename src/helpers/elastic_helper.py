# -*- coding: utf-8 -*-
from src.helpers.base_helper import BaseHelper
from elasticsearch import Elasticsearch

global_es = Elasticsearch()


class ElasticHelper(BaseHelper):
    
    def __init__(self):
        super().__init__()
        self.__global_es = global_es

    def get(self, index: str, doc_type: str, id: str):
        results = self.__global_es.get(index=index, doc_type=doc_type, id=id)
        return results['_source']

    def index(self, index: str, doc_type: str, id: str, schema):
        result = self.__global_es.index(index=index, doc_type=doc_type, id=id, body=schema)
        return result

    def search(self, query, fields):
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": fields
                }
            }
        }
        result = self.__global_es.search(index="contents", doc_type="title", body=body)

        return result['hits']['hits']


es = ElasticHelper()
