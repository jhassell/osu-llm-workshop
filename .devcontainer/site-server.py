#!/usr/bin/env python3
"""Serve ONE folder on port 8000, and nothing outside it.

Started detached by site-public.sh. Python's own `python3 -m http.server
--directory site` is not used here: it strips ".." from the URL path but never
resolves symlinks, so a single link inside site/ (say `ln -s ~ site/home`)
would publish whatever it points at, including .env (the labs key) and
~/.openclaw/openclaw.json (the same key, for OpenClaw), on a port that
site-public.sh makes public.

Every request is refused unless the real path of what it asks for is inside the
served folder. Names that start with a dot (.env, .git) are refused too, and
a folder without index.html gets 404, never a listing of its names. The
folder itself must be a real folder, not a symlink. site-check.py fails on a
symlink under site/, so this server and publish-site.sh agree about what the
site contains.

Every reply carries Cache-Control: no-store, so a refresh shows the newest
file, and X-Workshop-Site: 1, so site-public.sh can tell this server from
anything else listening on the port.

Usage: python3 .devcontainer/site-server.py <folder> [port] [bind address]
Adapted from jhassell/asee9 (CC BY 4.0).
"""
import http.server
import os
import sys
import urllib.parse

ARG = sys.argv[1] if len(sys.argv) > 1 else "site"
ROOT = os.path.realpath(ARG)
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
BIND = sys.argv[3] if len(sys.argv) > 3 else "0.0.0.0"


def inside(path):
    real = os.path.realpath(path)
    return real == ROOT or real.startswith(ROOT + os.sep)


def hidden(url_path):
    """True if any part of the URL path starts with a dot (.env, .git/...)."""
    path = urllib.parse.unquote(url_path.split("?", 1)[0].split("#", 1)[0])
    return any(part.startswith(".") for part in path.replace("\\", "/").split("/") if part)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Workshop-Site", "1")
        super().end_headers()

    def send_head(self):
        # The one hook both GET and HEAD go through, and it runs before the
        # parent's directory redirect and folder listing.
        if hidden(self.path) or not inside(self.translate_path(self.path)):
            self.send_error(404, "File not found")
            return None
        return super().send_head()

    def list_directory(self, path):
        # No folder listings: a listing would show the names of dotfiles and
        # symlinks to anyone with the address. GitHub Pages does not list
        # folders either, so the live site and the published one agree.
        self.send_error(404, "File not found")
        return None


def main():
    if os.path.islink(ARG.rstrip("/") or ARG):
        sys.stderr.write("site-server: %s is a symlink; refusing to serve it\n" % ARG)
        return 1
    if not os.path.isdir(ROOT):
        sys.stderr.write("site-server: no folder at %s\n" % ROOT)
        return 1
    server = http.server.ThreadingHTTPServer((BIND, PORT), Handler)
    sys.stderr.write("site-server: serving %s on port %d\n" % (ROOT, PORT))
    sys.stderr.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
