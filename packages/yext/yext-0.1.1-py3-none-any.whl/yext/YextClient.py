import requests
import json
from typing import List
from .AnswersUniversalResults import AnswersUniversalResults


class YextClient:

    """
    A class for making querying and interfacing with the Yext Live API and
    knowledge API easy.

    Args:
    ----
        api_key: str
            The API key for the account. (See developer console.)
            We may add a way to infer this for Answers experiences in the future.
        v: str, defaul `20200101`
            The version of the Live API as of this date. This does not affect
            Answers functionality, only other endpoints.
    """

    KNOWLEDGE_ENDPOINTS = {
        'PRODUCTION': {
            'list_entities': 'https://api.yext.com/v2/accounts/me/entities',
            'list_profiles': 'https://api.yext.com/v2/accounts/me/entityprofiles',
            'entities': 'https://api.yext.com/v2/accounts/me/entities',
            'entity': 'https://api.yext.com/v2/accounts/me/entities/{entity_id}',
            'profile': 'https://api.yext.com/v2/accounts/me/entityprofiles/{entity_id}/{locale}'
        }
    }
    ANSWERS_ENDPOINTS = {
        'PRODUCTION': {
            'answers_universal': 'https://liveapi.yext.com/v2/accounts/me/answers/query',
            'answers_vertical': 'https://liveapi.yext.com/v2/accounts/me/answers/vertical/query',
        },
        'SANDBOX': {
            'answers_universal': 'https://liveapi-sandbox.yext.com/v2/accounts/me/answers/query',
            'answers_vertical': 'https://liveapi-sandbox.yext.com/v2/accounts/me/answers/vertical/query',
        }
    }

    def __init__(self, api_key: str, v: str = '20200101',
                 env: str = 'PRODUCTION'):
        self.api_key = api_key
        self.env = env
        self.v = v

    def __repr__(self):
        return f'Yext API client, API key: {self.api_key}'

    def search_answers_vertical(self, query: str, experience_key: str,
                                vertical_key: str, locale: str = 'en',
                                version: str = 'PRODUCTION'):
        """
        Searches the Answers vertical search endpoint.

        Args:
        ----
            query: str
                The query string (what you'd type in the search bar).
            experience_key: str
                The key for the Answers experience.
            vertical_key: str
                The key for the vertical.
            locale: str, default `en`
                The locale to pass. This controls the language profiles
                returned as well as the query understanding behavior.
            version: str, default `PRODUCTION`
                The version of the experience. This can be `PRODUCTION`,
                `STAGING` or a number.
        """
        endpoint = self.ANSWERS_ENDPOINTS[self.env]['answers_universal']
        params = {
            'input': query,
            'api_key': self.api_key,
            'locale': locale,
            'v': self.v,
            'experienceKey': experience_key,
            'version': version,
            'verticalKey': vertical_key
        }
        response = requests.get(endpoint, params=params).json()
        return response

    def search_answers_universal(self, query: str, experience_key: str,
                                 locale: str = 'en',
                                 version: str = 'PRODUCTION'):
        """
        Searches the Answers universal search endpoint.

        Args:
        ----
            query: str
                The query string (what you'd type in the search bar).
            experience_key: str
                The key for the Answers experience.
            locale: str, default `en`
                The locale to pass. This controls the language profiles
                returned as well as the query understanding behavior.
            version: str, default `PRODUCTION`
                The version of the experience. This can be `PRODUCTION`,
                `STAGING` or a number.
        """
        endpoint = self.ANSWERS_ENDPOINTS[self.env]['answers_universal']
        params = {
            'input': query,
            'api_key': self.api_key,
            'locale': locale,
            'v': self.v,
            'experienceKey': experience_key,
            'version': version
        }
        response = requests.get(endpoint, params=params)
        results = AnswersUniversalResults(response)
        return results

    def get_all_entities(self, params: dict = {}) -> List[dict]:
        """
        :param params:
        :return:
        Fetch all of the entities within an account.
        """
        endpoint = self.KNOWLEDGE_ENDPOINTS[self.env]['list_entities']
        results = []
        page_token = ''
        while True:
            full_params = {
                'api_key': self.api_key,
                'v': '20200101',
                'limit': 50,
                **params
            }
            if page_token:
                params['pageToken'] = page_token
            response = requests.get(endpoint, full_params)
            if response.status_code != 200:
                error_text = response.text
                raise Exception('Invalid response: \n{}'.format(error_text))
            else:
                response = response.json()
            next_results = response['response']['entities']
            results += next_results
            if 'pageToken' in response['response']:
                page_token = response['response']['pageToken']
            else:
                break
        return results

    def create_entity(self, entity_type:str, profile: dict):
        """
        Creates an entity in the Knowledge Graph.

        Args:
        ----
            entity_type: str
                The API name of the entity type to create.
            profile: dict
                The JSON of the entity profile, including the `meta` which
                details the entity ID and country code, as well as the body
                where the keys are the API names of the fields.
        """
        params = {
            'entityType': entity_type,
            'api_key': self.api_key,
            'v': self.v
        }
        endpoint = self.KNOWLEDGE_ENDPOINTS[self.env]['entities']
        response = requests.post(endpoint, params=params, json=profile)
        response.raise_for_status()
        return response.json()

    def upsert_profile(self, entity_id: str, locale: str, profile_json: dict):
        """ Upsert a new language profile for a given entity. """
        endpoint = self.knowledge_endpoints['profile']
        endpoint = endpoint.format(entity_id=entity_id, locale=locale)
        params = {
            'api_key': self.api_key,
            'v': self.v,
            'format': 'html'  # In case of rich text fields.
        }
        response = requests.put(endpoint, params=params, json=profile_json)
        if str(response.status_code).startswith('2'):
            return response.json()
        else:
            error_text = response.text
            fmt_json = json.dumps(profile_json)
            msg = f'Invalid response: \n{error_text}\n Request: {fmt_json}'
            raise Exception(msg)
