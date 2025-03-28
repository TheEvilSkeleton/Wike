# This file is part of Wike (com.github.hugolabe.Wike)
# SPDX-FileCopyrightText: 2021-24 Hugo Olabera <hugolabe@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


from pathlib import Path
from libzim.reader import Archive

from gi.repository import Gio, Gtk, Adw, WebKit, GLib, GObject

from wike.data import settings
from wike.view import network_session


@Gtk.Template(resource_path='/com/github/hugolabe/Wike/gtk/archive-row.ui')
class ArchiveRow(Adw.ActionRow):
  __gtype_name__ = 'ArchiveRow'

  def __init__(self, archive, **kwargs):
    super().__init__(**kwargs)

    self.archive = archive

    self.set_title(archive.main_entry.title)

# Preferences dialog

@Gtk.Template(resource_path='/com/github/hugolabe/Wike/gtk/prefs.ui')
class PrefsDialog(Adw.PreferencesDialog):

  __gtype_name__ = 'PrefsDialog'

  start_combo = Gtk.Template.Child()
  tabs_switch = Gtk.Template.Child()
  desktop_switch = Gtk.Template.Child()
  history_switch = Gtk.Template.Child()
  clear_history_button = Gtk.Template.Child()
  data_switch = Gtk.Template.Child()
  archives_stack = Gtk.Template.Child()
  clear_data_button = Gtk.Template.Child()
  archives_list_box = Gtk.Template.Child()

  archives_dir = Path(GLib.get_user_data_dir()) / 'archives'

  # Connect signals and bindings

  def __init__(self, window):
    super().__init__()

    self._window = window

    settings.bind('on-start-load', self.start_combo, 'selected', Gio.SettingsBindFlags.DEFAULT)
    settings.bind('hide-tabs', self.tabs_switch, 'active', Gio.SettingsBindFlags.DEFAULT)
    settings.bind('search-desktop', self.desktop_switch, 'active', Gio.SettingsBindFlags.DEFAULT)
    settings.bind('keep-history', self.history_switch, 'active', Gio.SettingsBindFlags.DEFAULT)
    settings.bind('clear-data', self.data_switch, 'active', Gio.SettingsBindFlags.DEFAULT)

    self.clear_history_button.connect('clicked', self._clear_history_button_cb)
    self.clear_data_button.connect('clicked', self._clear_data_button_cb)

    archives = self.get_sorted_archives_list()
    if len(archives):
      self.archives_stack.set_visible_child_name('archives-list-page')
      self.__populate_archives(archives)

  def get_archive_uuid(self, archive):
    return str(archive.uuid)

  def get_sorted_archives_list(self):
    archives = []
    for archive in self.archives_dir.glob('*'):
      archives.append(Archive(str(archive)))
    return sorted(archives, key=self.get_archive_uuid)

  def __populate_archives(self, archives):
    for archive in archives:
      archive_row = ArchiveRow(archive)
      self.archives_list_box.append(archive_row)

  @Gtk.Template.Callback()
  def _on_import_insert_zim_archives_action_cb(self, *args):
    self._on_import_zim_archives_action_cb()

  @Gtk.Template.Callback()
  def _on_import_zim_archives_action_cb(self, *args):
    def load_archives_cb(dialog, result):
      try:
        files = file_dialog.open_multiple_finish(result)
      except GLib.GError:
        return
      self.archives_dir.mkdir(exist_ok=True)

      for file in files:
        uuid = str(Archive(file.get_path()).uuid)
        new_file = Gio.File.new_for_path(str(self.archives_dir / uuid))
        file.move(new_file, Gio.FileCopyFlags.NONE, None, None)

      self.archives_list_box.remove_all()
      archives = self.get_sorted_archives_list()
      self.__populate_archives(archives)

    file_filter_store = Gio.ListStore.new(Gtk.FileFilter)

    file_filter = Gtk.FileFilter.new()
    file_filter.add_mime_type('application/x-openzim')
    file_filter.set_name(_('ZIM Archives'))

    file_filter_store.append(file_filter)

    file_dialog = Gtk.FileDialog.new()
    file_dialog.set_modal(True)
    file_dialog.set_filters(file_filter_store)
    file_dialog.set_title(_('Select Archives'))
    file_dialog.open_multiple(self._window, callback=load_archives_cb)

  # Show clear history dialog

  def _clear_history_button_cb(self, clear_history_button):
    builder = Gtk.Builder()
    builder.add_from_resource('/com/github/hugolabe/Wike/gtk/dialogs.ui')
    clear_history_dialog = builder.get_object('clear_history_dialog')

    clear_history_dialog.connect('response', self._clear_history_response_cb)
    clear_history_dialog.present(self)

  # On response clear history

  def _clear_history_response_cb(self, dialog, response):
    if response == 'clear':
      self._window.history_panel.clear_history()

  # Show clear personal data dialog

  def _clear_data_button_cb(self, clear_data_button):
    builder = Gtk.Builder()
    builder.add_from_resource('/com/github/hugolabe/Wike/gtk/dialogs.ui')
    clear_data_dialog = builder.get_object('clear_data_dialog')

    clear_data_dialog.connect('response', self._clear_data_response_cb)
    clear_data_dialog.present(self)

  # On response clear personal data

  def _clear_data_response_cb(self, dialog, response):
    if response == 'clear':
      data_manager = network_session.get_website_data_manager()
      data_manager.clear(WebKit.WebsiteDataTypes.ALL, 0, None, None, None)
