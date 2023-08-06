#  Copyright  2020 Alexis Lopez Zubieta
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
import logging
import os

from appimagebuilder.app_dir.app_info.loader import AppInfoLoader
from appimagebuilder.app_dir.file_info_cache import FileInfoCache
from .app_run import AppRun
from .helpers.factory import HelperFactory
from ...recipe import Recipe


class RuntimeGeneratorError(RuntimeError):
    pass


class RuntimeGenerator:
    def __init__(self, recipe: Recipe, file_info_cache: FileInfoCache):
        self._configure(recipe)
        self.app_run_constructor = AppRun
        self.helper_factory_constructor = HelperFactory
        self.file_info_cache = file_info_cache

    def _configure(self, recipe):
        self.app_dir = recipe.get_item("AppDir/path")
        self.app_dir = os.path.abspath(self.app_dir)

        app_info_loader = AppInfoLoader()
        self.app_info = app_info_loader.load(recipe)
        self.apprun_version = recipe.get_item("AppDir/runtime/version", "v1.2.3")
        self.apprun_debug = recipe.get_item("AppDir/runtime/debug", False)
        self.env = recipe.get_item("AppDir/runtime/env", {})
        self.path_mappings = recipe.get_item("AppDir/runtime/path_mappings", [])

    def generate(self):
        app_run = self.app_run_constructor(
            self.apprun_version,
            self.apprun_debug,
            self.app_dir,
            self.app_info.exec,
            self.app_info.exec_args,
        )
        self._configure_runtime(app_run)
        self._add_user_defined_settings(app_run)

        self._set_path_mappings(app_run)

        app_run.deploy()

    def _configure_runtime(self, app_run):
        factory = self.helper_factory_constructor(self.app_dir, self.file_info_cache)
        for id in factory.list():
            h = factory.get(id)
            h.configure(app_run)

    def _add_user_defined_settings(self, app_run: AppRun) -> None:
        for k, v in self.env.items():
            if k in app_run.env:
                logging.info("Overriding runtime env: %s" % k)

            app_run.env[k] = v

    def _set_path_mappings(self, app_run: AppRun):
        if self.path_mappings:
            path_mappings_env = ""
            for path_mapping in self.path_mappings:
                path_mappings_env += path_mapping + ";"

            app_run.env["APPRUN_PATH_MAPPINGS"] = path_mappings_env
