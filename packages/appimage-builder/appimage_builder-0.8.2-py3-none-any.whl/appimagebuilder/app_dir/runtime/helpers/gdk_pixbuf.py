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
import subprocess
import shutil

from .base_helper import BaseHelper


class GdkPixbuf(BaseHelper):
    def configure(self, app_run):
        path = self._get_gdk_pixbuf_loaders_path()
        if path:
            loaders_cache_path = os.path.join(
                self.app_dir, os.path.dirname(path), "loaders.cache"
            )

            self._generate_loaders_cache(path, loaders_cache_path)

            app_run.env["GDK_PIXBUF_MODULEDIR"] = "$APPDIR/%s" % path
            app_run.env["GDK_PIXBUF_MODULE_FILE"] = loaders_cache_path.replace(
                self.app_dir, "$APPDIR"
            )
            app_run.env["APPDIR_LIBRARY_PATH"] = "$APPDIR/%s:%s" % (
                path,
                app_run.env["APPDIR_LIBRARY_PATH"],
            )

    def _generate_loaders_cache(self, loaders_path, loaders_cache_path):
        proc = subprocess.run(
            self._get_gdk_pixbuf_query_loaders_bin(),
            cwd=self.app_dir,
            stdout=subprocess.PIPE,
        )
        query_output = proc.stdout.decode("utf-8")

        logging.info("GDK loaders cache modules dir: %s" % loaders_path)
        modified_output = self._remove_loaders_path_prefixes(query_output.splitlines())

        with open(loaders_cache_path, "w") as f:
            f.write("\n".join(modified_output))

        logging.info("GDK loaders cache wrote to: %s" % loaders_cache_path)

    def _get_gdk_pixbuf_query_loaders_bin(self):
        for root, dirs, files in os.walk("/usr/lib"):
            if "gdk-pixbuf-query-loaders" in files:
                return os.path.join(root, "gdk-pixbuf-query-loaders")
        # we did not find gdk-pixbuf-query-loaders in /usr/lib
        # perhaps we should search /usr/bin too
        # Arch Linux has gdk-pixbuf-query-loaders in /usr/bin and
        # not in /usr/lib. This can be easily found out using
        # shutil.which API. => $PATH
        if shutil.which("gdk-pixbuf-query-loaders"):
            return shutil.which("gdk-pixbuf-query-loaders")
        raise RuntimeError("Missing 'gdk-pixbuf-query-loaders' executable")

    def _get_gdk_pixbuf_loaders_path(self):
        paths = self.app_dir_cache.find(
            "*/usr/*/gdk-pixbuf-2.0/*/loaders", attrs=["is_dir"]
        )
        if paths:
            rel_path = os.path.relpath(paths[0], self.app_dir)
            return rel_path

        return None

    def _remove_loaders_path_prefixes(self, loaders_cache):
        output = []
        for line in loaders_cache:
            if line.startswith('"/'):
                line = line.strip('"')
                line = os.path.basename(line)
                line = '"%s"' % line

            output.append(line)

        return output
