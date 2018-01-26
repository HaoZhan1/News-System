var rpc_client = require('./rpc_client');

rpc_client.add(5, 6, function(res) {
  console.log('success!! ' + res);
  console.assert(res == 11);
});
