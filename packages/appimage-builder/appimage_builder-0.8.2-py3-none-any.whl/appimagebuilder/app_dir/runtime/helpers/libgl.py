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

from .base_helper import BaseHelper


class LibGL(BaseHelper):
    def configure(self, app_run):
        dri_path = self._get_dri_path()
        if dri_path:
            app_run.env["LIBGL_DRIVERS_PATH"] = "$APPDIR/%s" % dri_path

    def _get_dri_path(self):
        paths = self.app_dir_cache.find("*/dri", attrs=["is_dir"])
        if paths:
            return os.path.relpath(paths[0], self.app_dir)
