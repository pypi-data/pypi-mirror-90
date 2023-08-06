# -*- coding: utf-8 -*-

from configparser import ConfigParser
from Products.Five import BrowserView
from plone import api

import requests
import transaction


class MigrationView(BrowserView):
    """
    Base class for licences browser views.
    """

    def __call__(self, **kwargs):
        site = api.portal.get()
        catalog = api.portal.get_tool('portal_catalog')
        config = Config('site_to_migrate')
        self.source_url = config.source['url']
        self.source_login = config.source['login']
        self.source_password = config.source['password']
        self.destination_url = config.destination['url']
        self.destination_login = config.destination['login']
        self.destination_password = config.destination['password']
        self.objects_to_finalize = {
            'collections': []
        }
        objects_tree = self.recursive_explore(self.source_url)
        if config.destination.pop('clean', False):
            self.clean_site(site)
            transaction.commit()
        self.recursive_create(self.destination_url, objects_tree=objects_tree['items'])
        self.finalize_collections(self.objects_to_finalize['collections'])
        catalog.clearFindAndRebuild()

    def recursive_explore(self, url):
        """
        Explore the whole site and return the whole tree of items an sub-items
        from the root 'url' as list of nested dicts.
        The sub-items are in the key 'items'.
        """
        headers = {'Accept': 'application/json'}
        auth = (self.source_login, self.source_password)
        resp = requests.get(url, headers=headers, auth=auth)
        container = resp.json()
        subobjects = container.pop('items', [])
        container['items'] = []
        print('exploring {}'.format(container['@id']))
        for subobject in subobjects:
            subobject_info = self.recursive_explore(subobject['@id'])
            container['items'].append(subobject_info)
        return container

    def clean_site(self, site):
        """
        Recursively delete all the objects starting from the root 'url'.
        """
        portal_types = site.portal_types
        for subobject in site.objectValues():
            if getattr(subobject.aq_base, 'portal_type', '') in portal_types.objectIds():
                print('deleted {}'.format(subobject.id))
                site.manage_delObjects([subobject.getId()])

    def recursive_create(self, url, objects_tree=[]):
        """ """
        portal = api.portal.get()
        portal_types = api.portal.get_tool('portal_types')
        workflow_tool = api.portal.get_tool('portal_workflow')
        headers = {'Accept': 'application/json'}
        destination_auth = (self.destination_login, self.destination_password)
        for obj_args in objects_tree:
            # ignore unknown content types
            if obj_args['@type'] not in portal_types.objectIds():
                continue
            sub_obj_tree = obj_args.pop('items', [])
#            if obj_args['@type'] in ['Image']:
#                source_auth = (self.source_login, self.source_password)
#                payload = requests.get(obj_args['image']['download'], headers=headers, auth=source_auth)
#                obj_args['image']['data'] = payload.content
            response = requests.post(url, headers=headers, auth=destination_auth, json=obj_args)
            created = response.json()
            print('created {}'.format(created['@id']))
            transaction.commit()

            # set previous state of created object
            created_object = self.context.restrictedTraverse(created['@id'].split(portal.id + '/')[-1])
            workflow_def = workflow_tool.getWorkflowsFor(created_object)
            if workflow_def:
                workflow_def = workflow_def[0]
                workflow_id = workflow_def.getId()
                workflow_state = workflow_tool.getStatusOf(workflow_id, created_object)
                workflow_state['review_state'] = obj_args['review_state']
                workflow_tool.setStatusOf(workflow_id, created_object, workflow_state.copy())

            if obj_args['@type'] in ['Collection']:
                self.objects_to_finalize['collections'].append(created_object)

            if obj_args['@type'] not in ['Collection']:
                # recursive call
                self.recursive_create(created['@id'], objects_tree=sub_obj_tree)

    def finalize_collections(self, collections):
        # for collections set the parent folder view as the collection result
        for collection in collections:
            parent = collection.aq_parent
            if parent.portal_type == 'Folder' and api.content.get_state(collection) == 'published':
                parent.setDefaultPage(collection.id)
                print('finalized collection folder {}'.format(parent.id))


class Config(object):
    """
    Parse a config file in the 'scripts' folder.
    The config file must content for source and destination :
    url, login and password for admin user.
    """
    def __init__(self, config_name):
        self.parser = None
        self.sections = {}
        parser = ConfigParser()
        parser.read('scripts/{}.cfg'.format(config_name))
        self.parser = parser
        for section in parser.sections():
            self.sections[section] = dict(self.parser.items(section))

    def __getattr__(self, attr_name):
        return self.section(attr_name)

    def section(self, section_name):
        return self.sections.get(section_name, {})
