var rest = require('../server/controllers/rest');

module.exports = function (app) {
	app.get('/api/search/:query', rest.findPeople);
	app.get('/api/profile/:id', rest.findPerson);
}