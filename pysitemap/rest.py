import inspect
from collections import OrderedDict

import json
from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_routedef import UrlDispatcher

from db import session, get_or_create
from models import Domain, DomainGroup

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class RestEndpoint:

    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)

        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})

        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            # Expected match info that doesn't exist
            raise HttpBadRequest('')

        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})


class DomainEndpoint(RestEndpoint):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self) -> Response:
        data = []

        domains = session.query(Domain).all()
        for instance in self.resource.collection.values():
            data.append(self.resource.render(instance))

        return Response(status=200, body=self.resource.encode({
            'domains': [
                {
                    'id': domain.id, 'title': domain.domain,
                    'groups': [{'id': group.id, 'name': group.name} for group in domain.groups]
                } for domain in session.query(Domain).all()
            ]}), content_type='application/json')

    async def post(self, request):
        data = await request.json()
        domain, _created = get_or_create(Domain, domain=data['domain'])

        return Response(status=200, body=self.resource.encode(
            {'id': domain.id, 'domain': domain.domain, 'created': _created},
        ), content_type='application/json')


class DomainGroupEndpoint(RestEndpoint):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self) -> Response:

        return Response(status=200, body=self.resource.encode({
            'domain_groups': [
                {
                    'id': group.id, 'name': group.name,
                    'domains': [{'id': domain.id, 'name': domain.domain} for domain in group.domains]
                } for group in session.query(DomainGroup).all()
            ]}), content_type='application/json')

    async def post(self, request):
        data = await request.json()
        group, _created = get_or_create(session, DomainGroup, name=data['name'])
        domains = []
        if data.get('domains'):
            for domain_el in data.get('domains'):
                domain, _domain_created = get_or_create(session, Domain, domain=domain_el)
                domains.append({'id': domain.id, 'domain': domain_el, 'created': _domain_created})

        return Response(
            status=200,
            body=self.resource.encode({
                'id': group.id,
                'name': group.name,
                'domains': domains,
                'created': _created
            }), content_type='application/json')


class RestResource:
    def __init__(self, notes, factory, collection, properties, id_field):
        self.notes = notes
        self.factory = factory
        self.collection = collection
        self.properties = properties
        self.id_field = id_field

        self.domain_endpoint = DomainEndpoint(self)
        self.domain_groups_endpoint = DomainGroupEndpoint(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/{domains}'.format(notes=self.notes), self.domain_endpoint.dispatch)
        router.add_route('*', '/{domain_groups}'.format(notes=self.notes), self.domain_groups_endpoint.dispatch)

    def render(self, instance):
        return OrderedDict((notes, getattr(instance, notes)) for notes in self.properties)

    @staticmethod
    def encode(data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))