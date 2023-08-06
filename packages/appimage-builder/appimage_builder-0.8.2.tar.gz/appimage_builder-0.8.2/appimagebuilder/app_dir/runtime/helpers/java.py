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


class Java(BaseHelper):
    class Error(RuntimeError):
        pass

    def configure(self, app_run):
        try:
            java_home = self._get_java_home_dir()
            app_run.env["JAVA_HOME"] = "$APPDIR/%s" % java_home
        except Java.Error:
            pass

    def _get_java_home_dir(self):
        java_bin = self.app_dir_cache.find("*/bin/java", attrs=["is_bin"])
        if not java_bin:
            raise Java.Error("Missing java binary")

        bin_dir = os.path.dirname(java_bin)
        java_home = os.path.dirname(bin_dir)
        rel_java_home = os.path.relpath(java_home, self.app_dir)

        return rel_java_home
