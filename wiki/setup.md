Help Page Setup
===============

Follow the below steps to make the web api help page available
at the root of the rptk web api server.
The documented steps assume that you are using [nginx](http://nginx.org).

1.  Download [mdwiki.html](http://dynalon.github.io/mdwiki/) into the
    root directory (`$WEBROOT`) of your webserver.
2.  Rename the mdwiki file:
    ```
    $ cd $WEBROOT
    $ mv mdwiki.html index.html
    ```
3.  Edit your webserver config to serve index.html by default before
    proxying to your WSGI server, e.g.:
    ```
    location / {
    try_files $uri $uri/index.html @uwsgi;
    }
    ```
4.  Symlink the contents of the rptk/wiki directory to `$WEBROOT`:
    ```
    ls -s $PATH/rptk/wiki/* $WEBROOT/
    ```
