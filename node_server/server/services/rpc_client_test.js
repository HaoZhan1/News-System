var rpc_client = require('./rpc_client');

rpc_client.add(5, 6, function(res) {
  console.log('success!! ' + res);
  console.assert(res == 11);
});

rpc_client.getNewsSummariesForUser('test_user', 1, function(response){
  console.log(response);
  console.assert(response != null);
});
