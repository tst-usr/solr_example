#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
import sys

import argparse
import collections
import configparser
import logging
import os
import random
import pandas
import requests
import time
import threading
from bs4 import BeautifulSoup
from post import SolrPost
import utils

from pdb import set_trace as bp


def parse_document(doc):
    elements = []
    children = doc.children

    for child in children:
        try:
            tag_name = child.name

            if not tag_name:
                continue

            if tag_name == "sec":
                temp_doc = parse_document(child)
                elements += temp_doc
            else:
                processed = "NOT SUPPORTED TAG TYPE"
                ordinal = -1

                if tag_name == "p" or tag_name == "title":
                    processed = child.text

                temp = [tag_name, str(child), processed, ordinal]
                elements.append(temp)
        except:
            print(sys.exc_info())

    return elements


def parse_head(doc):
    elements = []
    children = doc.children
    children = [c for c in children]

    res = {}

    for child in children:
        tag_name = child.name
        if tag_name == "article-meta":
            title = child.findChildren("related-article")[0].text
            res["title"] = title
        elif tag_name == "journal-meta":
            journal = child.findChildren("journal-title")[0].text
            res["journal"] = journal

    return res


def simple_preproc(path):
    count = 0
    files = utils.get_all_files(corpus_path, ".xml")
    total = len(files)
    res = pandas.DataFrame()

    for _file in files:
        print(count, total)
        try:
            count += 1
            doc_lines = ""
            file_path = os.path.join(_file["path"], _file["title"])

            with open(file_path, mode="r") as _f:
                doc_lines = _f.read()

            xmldoc = BeautifulSoup(doc_lines, 'html.parser')
            front = xmldoc.front
            body = xmldoc.body

            head = parse_head(front)
            parsed_doc = parse_document(body)

            docdf = pandas.DataFrame(parsed_doc, columns=[
                                     "tag", "original", "processed", "ordinal"])
            docdf["title"] = head["title"]
            docdf["journal"] = head["journal"]

            res = pandas.concorpocat([res, docdf])
        except:
            print("ex")
            logger = logging.getLogger("EXCEPTION")
            logger.info(sys.exc_info())

    return res


def index_data(indexer, csv_file):
    """
    In this example we load from csv which contains
    plain text fields and then we index using http rest method
    with the data structure that corresponds to a single field in
    schema of Solr instance

    We use searcher instance of Solr which doesn't have attr_content field
    configured

    Parameters
    ----------
    csv_file : str
        filepath of csv to load
    """
    df = pandas.read_csv(csv_file)
    count = 1

    documents = [doc for doc in df.iterrows()]
    total = len(documents)

    for document in documents:
        try:
            count += 1

            if count % 100 == 0:
                print(count, " of ", total, " documents indexed")

            doc = document[1]
            data = {'tag': doc["tag"],
                    'title': doc["title"],
                    'original':  doc["processed"],
                    'content': doc["processed"],
                    'journal': doc["journal"], }

            indexer.post_text("searcher", data)
        except Exception as ex:
            pass


def index_pdf(indexer, corpus_path):
    """
    In this example we take all PDF files in corpus path
    and index through solr cell method.

    By default, we use attr_content field to extract plain text of PDF

    Then in solr schema we copy the content in this field to other ones
    that process text on its own way

    We use pdf instance of Solr which has attr_content field configured

    Parameters
    ----------
    corpus_path : str
        folder where PDF are stored
    """
    count = 1
    files = utils.get_all_files(corpus_path, ".pdf")
    total = len(files)

    for _file in files:
        try:
            count += 1
            print(count, " of ", total, " documents indexed")

            file_path = os.path.join(_file["path"], _file["title"])
            indexer.index_by_document("pdf", **{
                "path": file_path,
                "title": _file["title"]
            })

        except:
            pass


if __name__ == "__main__":
    conf_parser = argparse.ArgumentParser(
        description=__doc__,  # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Turn off help, so we print all options in response to -h
        add_help=False
    )

    conf_parser.add_argument("-i", "--index_method",
                             help="Way to index, options: data, pdf",
                             metavar="FILE")
    conf_parser.add_argument("-cp", "--corpus_path",
                             help="Path of files to index", metavar="FILE")

    conf_parser.add_argument("-u", "--uri",
                             help=f"Uri of solr instance, if nothing changes"
                             f"in example: http://localhost:8984/solr",
                             metavar="FILE")

    conf_args, remain = conf_parser.parse_known_args()

    corpus_path = conf_args.corpus_path or "index/corpora"
    solr_uri = conf_args.uri or "http://localhost:8984/solr"

    indexer = SolrPost(solr_uri)

    if conf_args.index_method == "data":
        index_data(indexer, corpus_path)
    elif conf_args.index_method == "pdf":
        index_pdf(indexer, corpus_path)
    else:
        print("Method to index not allowed")
