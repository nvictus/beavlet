heroku config:set LIBRARY_PATH=/app/.heroku/vendor/lib  --app $1
heroku config:set LD_LIBRARY_PATH=/app/.heroku/vendor/lib  --app $1
heroku config:set PATH=bin:app/.heroku/venv/bin:/bin:/usr/local/bin:/usr/bin --app $1
heroku config:set BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git --app $1