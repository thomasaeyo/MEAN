var express = require('express');
var compression = require('compression');
var bodyParser = require('body-parser');
var methodOverride = require('method-override');

module.exports = function (app, config) {
	var env = process.env.NODE_ENV || 'development';
	if('development' == env) {
		app.use(compression());
		app.set('port', config.port);
		app.use(bodyParser.json());
		app.use(methodOverride());

		app.use('/', express.static(__dirname + "/../client/"));
	}
};