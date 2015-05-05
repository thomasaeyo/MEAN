var express = require('express');
var mongoose = require('mongoose');
var fs = require('fs');
var http = require('http');
var config = require('./config/config');
var root = __dirname;
var app = express();
var server = null;

// configure Mongoose by using db.js
require('./config/db')(config);

// dynamically load all models
var modelsPath = root + '/server/models';
fs.readdirSync(modelsPath).forEach(function (file) {
	if (file.indexOf('.js') >= 0) {
		require(modelsPath + '/' + file);
	}
});

// configure express
require('./config/express')(app, config);

// routes
require('./config/routes')(app);

// start the server
var server = http.createServer(app);
server.listen(config.port, config.host);
console.log('App started on port ' + config.port);