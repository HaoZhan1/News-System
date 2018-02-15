var jayson = require('jayson')

//use jayson to construct client and callback function
var client = jayson.client.http({
  hostname: 'localhost',
  port : 4041
});

function add(a, b, callback) {
  client.request('add', [a, b], function(err, response) {
    if (err) throw err;
    callback(response.result);
  })
};

function getNewsSummariesForUser(user_id, page_num, callback) {
  client.request('getNewsSummariesForUser',[user_id, page_num], function(err, res) {
    if (err) throw err;
    callback(res.result);
  });
};

function logNewsClickForUser(user_id, news_id) {
  client.request('logNewsClickForUser', [user_id, news_id], function(err, res) {
    if (err) throw err;
    console.log(res);
  });
};
module.exports = {
  add: add,
  getNewsSummariesForUser:getNewsSummariesForUser,
  logNewsClickForUser: logNewsClickForUser
}
