var express = require('express');
var router = express.Router();
var path = require('path');
var rpc_client = require('../services/rpc_client');
router.get('/', function(req, res, next) {
  news = [];
  res.json(news);
})

router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
  console.log("Fetching news...");
  user_id = req.params['userId'];
  page_num = req.params['pageNum'];
  console.log("Nodejs===");
  console.log(user_id);
  console.log(page_num);
  rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
      res.json(response);
  });
});
router.post('/userId/:userId/newsId/:newsId', function(req, res, next) {
  console.log("Logging news click...");
  user_id = req.params['userId']
  news_id = req.params['newsId']
  rpc_client.logNewsClickForUser(user_id, news_id);
  res.status(200);
});
module.exports = router;
