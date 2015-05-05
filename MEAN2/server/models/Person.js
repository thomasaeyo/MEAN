var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var Person = new Schema({
	first_name: String,
	last_name: String,
	facebook_url: String,
	twitter_url: String,
	linkedin_url: String,
	img_url: String,
	jobs: [{title: String, organization: String}],
	location: String,
	experiences: [{title: String, organization: String}],
	educations: [{school: String, major: String, degree_type: String, graduation_year: String}],
	news: [{title: String, author: String, url: String}],
	keywords: [{keyword: String, relevance: Number}],
});

mongoose.model('Person', Person);