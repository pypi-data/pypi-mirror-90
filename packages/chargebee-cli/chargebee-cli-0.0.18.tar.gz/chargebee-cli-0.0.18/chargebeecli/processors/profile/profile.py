from abc import ABC

from requests import Response

from chargebeecli.Configuration import Configuration
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator
import json


class Profile(Processor, Validator, ResponseFormatter, ABC):

    def __init__(self):
        self.response = None
        self.headers = self.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["name", "api_key", "account"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'profile', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Profile, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        response = Response()
        response.status_code = 200
        if resource_id is None:
            __active_profile = Configuration.Instance().fetch_section('active_profile', 'primary')
        else:
            __active_profile = resource_id
            if __active_profile not in Configuration.Instance().fetch_available_sections():
                exit()

        if __active_profile is None:
            return response
        res = {"profile": {"name": __active_profile,
                           "api_key": Configuration.Instance().fetch_section(__active_profile, "api_key"),
                           "account": Configuration.Instance().fetch_section(__active_profile, "account")}}
        response._content = json.dumps(res).encode('utf-8')
        return response

    def list(self, ctx):
        response = Response()
        response.status_code = 200
        __sections = Configuration.Instance().fetch_available_sections()
        if len(__sections) == 0:
            return response

        res = []
        for __profile in __sections:

            if __profile == 'active_profile': continue
            t = {"name": __profile, "api_key": Configuration.Instance().fetch_section(__profile, "api_key"),
                 "account": Configuration.Instance().fetch_section(__profile, "account")}
            t1 = {"profile": t}
            res.append(t1)

        t = {"list": res}

        response._content = json.dumps(t).encode('utf-8')
        return response

    def delete(self, ctx, payload, resource_id):
        response = Response()
        response.status_code = 200
        response._content = json.dumps({'profile': {'name': resource_id, 'message': 'deleted'}}).encode('utf-8')
        Configuration.Instance().delete_section_or_profile(resource_id)
        return response
