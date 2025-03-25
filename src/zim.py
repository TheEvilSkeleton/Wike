# This file is part of Wike (com.github.hugolabe.Wike)
# SPDX-FileCopyrightText: 2021-24 Hugo Olabera <hugolabe@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
import contextlib
import urllib.parse

from bs4 import BeautifulSoup
from libzim.search import Query, Search, Searcher
from wike.wiki import Wiki
from wike.data import session, settings
from gi.repository import Soup, GLib

class ZIM(Wiki):
  def __init__(self, base_uri_elements, archive):
    self.base_uri_elements = base_uri_elements
    self.archive = archive

  def get_random(self, callback):
    base_uri = urllib.parse.urlunparse(self.base_uri_elements)
    # libzim.archive.Archive.get_random_entry() is only available on a fork:
    # https://github.com/TheEvilSkeleton/python-libzim/commit/334d296df6de9b44a5176a184e8c4a591947a32e
    callback(None, base_uri + self.archive.get_random_entry().path, None)

  # Search Wikipedia with a limit of responses

  def search(self, text, lang, limit, callback):
    searcher = Searcher(self.archive)
    query = Query().set_query(text)
    search = searcher.search(query)

    # NOTE: The camelCase attributes are planned to be removed,
    #       so we're supporting the upcoming snake_case as a fallback
    #       for forward compatibility:
    #
    # https://github.com/openzim/python-libzim/pull/212
    try:
      results = search.getResults(0, limit)
    except AttributeError:
      results = search.get_results(0, limit)

    callback(None, results, None)

    return search

  def search_result(self, async_result):
    base_uri = urllib.parse.urlunparse(self.base_uri_elements)
    title_list = []
    uri_list = []
    for path in async_result:
      title_list.append(self.archive.get_entry_by_path(path).title)
      uri_list.append(base_uri + path)
    return (title_list, uri_list)

  def get_properties(self, page, callback, user_data):
    path = page.split(os.sep, maxsplit=2)[-1]

    try:
      entry = self.archive.get_entry_by_path(path)
    except KeyError:
      entry = self.archive.get_entry_by_path(self.archive.main_entry.path)

    item = entry.get_item()

    soup = BeautifulSoup(str(item.content, 'utf8'), "html.parser")

    properties = {}
    properties['title'] = entry.title
    properties['langlinks'] = []
    sections = []

    every_html_heading_except_h1 = re.compile(r'^h(?!(?:1)$)\d$')
    for tag in soup.find_all(every_html_heading_except_h1):
      level = int(tag.name[1])
      metadata = {}
      metadata['toclevel'] = level - 1
      try:
        id = tag.get_attribute_list('id')[0]
        metadata['anchor'] = id
      except IndexError:
        metadata['anchor'] = ''
      sections.append(metadata)

    properties['sections'] = sections

    if callback:
      callback(None, properties, None)

