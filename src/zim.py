# This file is part of Wike (com.github.hugolabe.Wike)
# SPDX-FileCopyrightText: 2021-24 Hugo Olabera <hugolabe@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import urllib.parse

from libzim.search import Query, Search, Searcher
from wike.wiki import Wiki
from wike.data import session, settings
from gi.repository import Soup

class ZIM(Wiki):
  def __init__(self, base_uri_elements, archive):
    self.base_uri_elements = base_uri_elements
    self.archive = archive

  def get_random(self, lang, callback):
    ...

  # Get random result from response data

  def random_result(self, async_result):
    ...

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
