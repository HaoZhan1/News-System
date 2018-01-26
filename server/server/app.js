var express = require('express');
var path = require('path');
var index = require('./routes/index');
var news = require('./routes/news');
var app = express();

// view engine setup
app.set('views', path.join(__dirname, '../../tap-news/build'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../../tap-news/build/static')));

app.use('/', index);
app.use('/news', news);

module.exports = app;
