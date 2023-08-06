# -*- coding: utf-8 -*-
"""rackio_opcua/worker.py

This module implements the worker for RackioOPCUA.
"""
import time

from threading import Thread


class OCPUAWorker(Thread):

    def __init__(self, core, *args, **kwargs):

        super(OCPUAWorker, self).__init__(*args, **kwargs)

        self.core = core
        self._stop = False

    def stop(self):

        self._stop = True

    def restart(self):

        self.stop_updaters()
        self.start_updaters()

    def start_updaters(self):

        for updater in self.core.get_mappings():

            updater.start()

    def stop_updaters(self):

        for updater in self.core.get_mappings():

            updater.stop()

    def run(self):

        server = self.core.server

        server.start()

        self.start_updaters()

        while not self._stop:

            time.sleep(0.25)

        self.stop_updaters()

        server.stop()
