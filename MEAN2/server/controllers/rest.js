var mongoose = require('mongoose');
var Person = mongoose.model('Person');

// return query results
exports.findPeople = function(req, res) {
	Person.find(
		{'keywords': {$elemMatch: {keyword: req.params.query.toLowerCase()}}},
		function(err, people) {
			if (err) {
				throw new Error(err);
			}
			res.send(people);
		})
};

// return the person's profile
exports.findPerson = function(req, res) {
	Person.findById(req.params.id, function(err, person) {
		if (err) {
			throw new Error(err);
		}

		keywords_inter(person, function(people_in_network) {
			var data = {
				'person': person, 
				'people_in_network': people_in_network
			};
			res.send(data);
		})
	});
};

// returns a set of people who share at least one common keyword
function keywords_inter(person, callback) {
	var keywords_list = [];

	for (var i = 1; i < person.keywords.length; i++) {
		keywords_list.push(person.keywords[i].keyword);	
	}

	Person.find(
		{'keywords': {$elemMatch: {keyword: {$in: keywords_list}}}}, 
		{'first_name': 1, 'last_name': 1, 'img_url': 1}, function(err, people) {
			if (err) {
				throw new Error(err);
			}
			callback(people);
		})
}