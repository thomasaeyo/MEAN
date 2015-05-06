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
		console.log(person);
		res.send(person);
	});
};