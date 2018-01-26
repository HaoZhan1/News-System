var jayson = require('jayson')

//use jayson to construct client and callback function
var client = jayson.client.http({
  hostname: 'localhost',
  port : 4040
});

function add(a, b, callback) {
  client.request('add', [a, b], function(err, response) {
    if(err) throw err;
    callback(response.result);
  })
}

module.exports = {
  add: add
}
