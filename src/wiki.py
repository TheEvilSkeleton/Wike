# This file is part of Wike (com.github.hugolabe.Wike)
# SPDX-FileCopyrightText: 2021-24 Hugo Olabera <hugolabe@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

class Wiki:
  base_uri_elements = ...

  def get_is_internal(self, uri_elements):
    return self.base_uri_elements.netloc == uri_elements.netloc

  def get_base_uri(self, uri_elements):
    return (uri_elements.scheme, uri_elements.netloc, uri_elements.path, '', '', '')

  def get_main_uri(self):
    raise NotImplementedError

  def get_language(self):
    raise NotImplementedError

  def get_random_page(self):
    raise NotImplementedError

  def search(self, string):
    raise NotImplementedError

  # def get_random(lang, callback):
  #   raise NotImplementedError

  # def random_result(async_result):
  #   raise NotImplementedError

  # def search(text, lang, limit, callback):
  #   raise NotImplementedError

  # def search_result(async_result):
  #   raise NotImplementedError

  def get_properties(self, page, callback, user_data):
    raise NotImplementedError

  def properties_result(async_result):
    raise NotImplementedError

