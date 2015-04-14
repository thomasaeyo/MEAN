var express = require('express');
var app = express();
var mongojs = require('mongojs');
var db = mongojs('personafi',['people']);
var bodyParser = require('body-parser');

app.use(express.static(__dirname + "/public"));
app.use(bodyParser.json());

app.post('/search', function (req, res) {
	// db.people.find(function (err, docs) {
	// 	console.log(docs);
	// });
	console.log("I received a POST request")
	console.log(req.body['query']);
	var keyword = 'keywords.'+String(req.body['query']);
	console.log(keyword);
	var query = {};
	query['keywords.'+req.body['query']] = { $exists: true };
	db.people.find(query, function (err, docs) {
		console.log(docs);
		res.json(docs);
	});
});

app.listen(3000);
console.log("Server running on port 3000");