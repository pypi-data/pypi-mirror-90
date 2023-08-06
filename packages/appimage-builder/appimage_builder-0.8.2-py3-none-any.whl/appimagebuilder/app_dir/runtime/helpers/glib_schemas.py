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
import os
import subprocess

from .base_helper import BaseHelper


class GLibSchemas(BaseHelper):
    def configure(self, app_run):
        path = self._get_glib_schemas_path()
        if path:
            subprocess.run(["glib-compile-schemas", path], cwd=self.app_dir)
            app_run.env["GSETTINGS_SCHEMA_DIR"] = "$APPDIR/%s" % path

    def _get_glib_schemas_path(self):
        paths = self.app_dir_cache.find(
            "*/usr/share/glib-2.0/schemas", attrs=["is_dir"]
        )
        if paths:
            rel_path = os.path.relpath(paths[0], self.app_dir)
            return rel_path
