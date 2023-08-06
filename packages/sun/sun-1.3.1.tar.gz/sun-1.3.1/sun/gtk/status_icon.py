#!/usr/bin/python3
# -*- coding: utf-8 -*-

# sun_gtk is a part of sun.

# Copyright 2015-2021 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# sun is a tray notification applet for informing about
# package updates in Slackware.

# https://gitlab.com/dslackw/sun

# sun is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
import subprocess
from sun.licenses import lic, abt
from sun.__metadata__ import (
    __all__,
    __email__,
    __author__,
    __version__,
    __website__,
    bin_path,
    icon_path
)
from sun.cli.tool import check_updates, daemon_status
from sun.utils import os_info


class GtkStatusIcon:

    def __init__(self):
        self.sun_icon = f'{icon_path}{__all__}.png'
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_file(self.sun_icon)
        self.status_icon.connect('popup-menu', self.right_click_event)
        self.cmd = f'{bin_path}sun_daemon'
        self.init_daemon()

    def init_daemon(self):
        '''Start daemon when gtk loaded'''
        if daemon_status() == 'SUN not running':
            subprocess.call(f'{self.cmd} &', shell=True)
            return 'Daemon Starts'
        else:
            return 'Daemon is already running...'

    def right_click_event(self, icon, button, time):
        '''Handler menu and submenu'''

        # Set Gtk menu and submenu
        self.menu = Gtk.Menu()
        submenu = Gtk.Menu()

        # Creating Start submenu handler
        img_start = Gtk.Image()
        img_start.set_from_stock(Gtk.STOCK_MEDIA_PLAY, 1)
        start = Gtk.ImageMenuItem('Start')
        start.connect('activate', self.daemon_start)
        start.set_image(img_start)

        # Creating Stop submenu handler
        img_stop = Gtk.Image()
        img_stop.set_from_stock(Gtk.STOCK_MEDIA_STOP, 1)
        stop = Gtk.ImageMenuItem('Stop')
        stop.connect('activate', self.daemon_stop)
        stop.set_image(img_stop)

        # Creating Restart submenu handler
        img_restart = Gtk.Image()
        img_restart.set_from_stock(Gtk.STOCK_REFRESH, 1)
        restart = Gtk.ImageMenuItem('Restart')
        restart.connect('activate', self.daemon_restart)
        restart.set_image(img_restart)

        # Creating Status submenu handler
        img_status = Gtk.Image()
        img_status.set_from_stock(Gtk.STOCK_PROPERTIES, 1)
        status = Gtk.ImageMenuItem('Status')
        status.connect('activate', self.show_daemon_status)
        status.set_image(img_status)

        # Creating the submenu fot the daemon
        submenu.append(start)
        submenu.append(stop)
        submenu.append(restart)
        submenu.append(status)
        img_daemon = Gtk.Image()
        img_daemon.set_from_stock(Gtk.STOCK_PREFERENCES, 1)
        daemon = Gtk.ImageMenuItem('Daemon')
        daemon.set_submenu(submenu)
        daemon.set_image(img_daemon)
        self.menu.append(daemon)

        # Creating Check Updates menu handler
        img_check = Gtk.Image()
        img_check.set_from_stock(Gtk.STOCK_OK, 1)
        check = Gtk.ImageMenuItem('Check Updates')
        check.connect('activate', self.show_check_updates)
        check.set_image(img_check)
        self.menu.append(check)

        # Creating Os Info menu handler
        img_info = Gtk.Image()
        img_info.set_from_stock(Gtk.STOCK_INFO, 1)
        osInfo = Gtk.ImageMenuItem('Os Info')
        osInfo.connect('activate', self.show_os_info)
        osInfo.set_image(img_info)
        self.menu.append(osInfo)

        # Creating seperator
        sep = Gtk.SeparatorMenuItem()
        self.menu.append(sep)

        # Creating About menu handler
        img_about = Gtk.Image()
        img_about.set_from_stock(Gtk.STOCK_ABOUT, 1)
        about = Gtk.ImageMenuItem('About')
        about.connect('activate', self.show_about_dialog)
        about.set_image(img_about)
        self.menu.append(about)

        # Creating Quit menu handler
        img_quit = Gtk.Image()
        img_quit.set_from_stock(Gtk.STOCK_QUIT, 1)
        quit = Gtk.ImageMenuItem('Quit')
        quit.connect('activate', Gtk.main_quit)
        quit.set_image(img_quit)
        self.menu.append(quit)

        self.menu.show_all()

        self.menu.popup(None, None, None, self.status_icon, button, time)

    def message(self, data, title):
        '''Method to display messages to the user'''
        msg = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                buttons=Gtk.ButtonsType.CLOSE)
        msg.set_resizable(0)
        msg.set_title(title)
        msg.format_secondary_text(data)
        msg.set_icon_from_file(self.sun_icon)
        msg.run()
        msg.destroy()

    def show_check_updates(self, widget):
        '''Show message updates'''
        title = 'SUN - Check Updates'
        data, packages = check_updates()
        count = len(packages)
        if count > 0:
            packages = packages[:10]
            if count > 10:
                packages += ['\nand more...']
            self.message('{0}\n{1}'.format(data, '\n'.join(packages)), title)
        else:
            self.message(data, title)

    def show_os_info(self, widget):
        '''Show message OS info'''
        title = 'SUN - OS Info'
        data = os_info()
        self.message(data, title)

    def show_about_dialog(self, widget):
        '''Show message About info'''
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name('SUN - About')
        about_dialog.set_icon_from_file(self.sun_icon)
        about_dialog.set_program_name('SUN')
        about_dialog.set_version(__version__)
        about_dialog.set_authors([f'{__author__} <{__email__}>'])
        about_dialog.set_license('\n'.join(lic))
        about_dialog.set_website(__website__)
        about_dialog.set_logo(Pixbuf.new_from_file(self.sun_icon))
        about_dialog.set_comments(abt)
        about_dialog.run()
        about_dialog.destroy()

    def daemon_start(self, widget):
        '''Show message and start the daemon'''
        title = 'Daemon'
        data = self.init_daemon()
        self.message(data, title)

    def daemon_stop(self, widget):
        '''Show message and stop the daemon'''
        title = 'Daemon'
        subprocess.call('killall sun_daemon', shell=True)
        data = 'Daemon stops'
        self.message(data, title)

    def daemon_restart(self, widget):
        '''Show message and restart the daemon'''
        title = 'Daemon'
        subprocess.call('killall sun_daemon', shell=True)
        subprocess.call(f'{self.cmd} &', shell=True)
        data = 'Daemon restarts'
        self.message(data, title)

    def show_daemon_status(self, widget):
        '''Show message status about the daemon'''
        title = 'Daemon'
        data = daemon_status()
        self.message(data, title)