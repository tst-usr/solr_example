#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import json
import re
import urllib
import urllib.request


class SolrPost:
    """
    Class for making petitions to solr
    ...

    Attributes
    ----------
    solr_url : str
        url address of solr instance

    Methods
    -------
    select(solr_core, query)
        Selects from core and retrieves a json with the info asked

    post_text(solr_core, data)
        Post a dict of text values to solr core

    commit(solr_core)
        Makes a commit to solr core

    """

    def __init__(self, solr_url):
        """
        Parameters
        ----------
        solr_url : str
            url address of solr instance
        """
        self.solr_url = solr_url \
            if solr_url.endswith("/") \
            else solr_url + "/"

    def __fix_name(self, name):
        if " " in name:
            name = name.replace(" ", "%20")

        name = re.sub('[\x80-\xFF]', lambda c: '%%%02x' %
                      ord(c.group(0)), name)

        return name

    def select(self, solr_core, query="q=*:*"):
        """
        Selects, using a query, from core and retrieves a json with info asked

        Parameters
        ----------
        solr_core : str
            name of the core to ask for
        query: str
            query for document selection, default value is q=*:*
        """

        try:
            query = self.__fix_name(query)

            solr_core = solr_core \
                if solr_core.endswith("/") \
                else solr_core + "/"

            request = urllib.request.Request(
                url=self.solr_url +
                solr_core +
                "select?" +
                query +
                "&wt=json"
            )

            return json.load(urllib.request.urlopen(request))
        except Exception as ex:
            print(ex)

    def post_text(self, solr_core, data):
        """
        Post a dict of text values to solr core

        Parameters
        ----------
        solr_core : str
            name of the core to ask for
        data: dict
            data must be formated as field:value, i.e. doc_id:1
        """
        try:
            if type(data) is not dict:
                raise ValueError('Data must be dict type')

            solr_core = "".join(solr_core.split("/")[-1]) \
                if solr_core.endswith("/") \
                else solr_core

            data = json.dumps([data])

            req = urllib.request.Request(
                url=self.solr_url + solr_core +
                '/update?commit=false' +
                "&wt=json")

            req.data = data.encode("utf-8")
            req.add_header('Content-type', 'application/json')

            f = urllib.request.urlopen(req)
            f.close()
        except Exception as ex:
            print(ex)

    def index_by_document(self, solr_core, **kwargs):
        filename = kwargs['path']
        title = self.__fix_name(kwargs['title'])
        type_document = kwargs.get("type", None) or "NA"

        try:
            with open(filename, 'rb') as data_file:
                my_data = data_file.read()

            title = self.__fix_name(title)
            filename = self.__fix_name(filename)

            req = urllib.request.Request(
                url=self.solr_url +
                solr_core +
                '/update/extract?' +
                '&literal.file_path=' + str(self.__fix_name(filename)) +
                '&literal.stream_name=' + str(title) +
                '&literal.type_document=' + str(type_document) +
                '&fmap.content_type_hint=omit' +
                '&commit=false',
                data=my_data)

            req.add_header('Content-type', 'application/pdf')
            f = urllib.request.urlopen(req)
            f.close()
        except Exception as ex:
            print(ex)

    def commit(self, solr_core):
        """
        Makes a commit to solr core to update and make available info indexed

        Parameters
        ----------
        solr_core : str
            name of the core to ask for
        """

        try:
            solr_core = solr_core \
                if solr_core.endswith("/") \
                else solr_core + "/"
        except Exception as ex:
            print(ex)
