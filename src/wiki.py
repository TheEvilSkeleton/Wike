# This file is part of Wike (com.github.hugolabe.Wike)
# SPDX-FileCopyrightText: 2021-24 Hugo Olabera <hugolabe@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

class Wiki:
  def get_language(self):
    ...

  def get_random_page(self):
    ...

  def search(self, string):
    ...

  # def get_random(lang, callback):
  #   raise NotImplementedError

  # def random_result(async_result):
  #   raise NotImplementedError

  # def search(text, lang, limit, callback):
  #   raise NotImplementedError

  # def search_result(async_result):
  #   raise NotImplementedError

  # def get_properties(page, lang, callback, user_data):
  #   raise NotImplementedError

  # def properties_result(async_result):
  #   raise NotImplementedError

