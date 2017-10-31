#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Autor Gustavo RPS
#  You can contact me by email (developers+gustavorps@labic.net)

import os

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import (TransportError, 
                           ConnectionTimeout, 
                           ConnectionError, 
                           NotFoundError,
                           RequestError,)


ES_HOST = os.environ['ES_HOST_URI_00']


class ElasticsearchEngine(object):
  """
  base of IndexTypeDocument based on mongoengine.Document
  """
  # def __init__(self, db, alias='default', **kwargs):
  def __init__(self, hosts=[]):
    try:
      if len(hosts) > 0:
        self.client = Elasticsearch([host])
      else:
        _kargs = {
          'maxsize': 25, 
          'send_get_body_as': 'POST',
        }
        self.client = Elasticsearch([ES_HOST], **_kargs)
    except ImproperlyConfigured as e:
      # TODO: handler properly
      raise e
    except ConnectionError as e:
      # TODO: handler properly
      raise e
    except ConnectionTimeout as e:
      # TODO: handler properly
      raise e

  def insert(index:str, 
             type:dict, 
             doc_or_docs:[dict], 
             load_bulk=True, 
             **kwargs:dict):
      try:
        if load_bulk:
          actions = []; append_action = actions.append
          for doc in docs:
            action = {
              '_index': index,
              '_type': type,
              '_source': doc,
            }
            source = {**doc, **action}
            
            append_action(source)

            result = helpers.bulk(self.client, **kwargs)
        else:
          action_create = {
            'index': index,
            'doc_type': type,
            'body': doc_or_docs,

          }
          self.client.create(doc_or_docs)
      # except Exception as elasticsearch.TransportError:
      #   # TODO: handler properly
      #   raise e
      except Exception as TransportError:
        # TODO: handler properly
        raise e
      except Exception as TransportError:
        # TODO: handler properly
        raise e
        
__all__ = [ElasticsearchEngine]