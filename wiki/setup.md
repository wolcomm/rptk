RPTK Web API Help Page Setup
============================

Follow the below steps to make the web api help page available
at the root of the rptk web api server.
The following steps assume that you are using [nginx](http://nginx.org) as your
webserver.
`$PREFIX` is the installation prefix (as determined by Python's `sys.prefix`) of
your `rptk` installation.
`$WEBROOT` is the `root` directory of your webserver, by default `/usr/share/nginx/html`.

1.  Download [mdwiki.html](http://dynalon.github.io/mdwiki/) into the webserver
    root directory:
    ```
    $ wget -O $WEBROOT/index.html http://dynalon.github.io/mdwiki/mdwiki-latest.html
    ```
2.  Edit your webserver config to serve index.html by default before
    proxying to your WSGI server, e.g.:
    ```
    location / {
    try_files $uri $uri/index.html @uwsgi;
    }
    ```
3.  Symlink the contents of the `share/rptk/html` directory to `$WEBROOT`:
    ```
    $ ln -s $PREFIX/share/rptk/html/* $WEBROOT/
    ```
