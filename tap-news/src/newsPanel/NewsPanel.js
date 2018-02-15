import React from 'react';
import './NewsPanel.css';
import _ from 'lodash';
import NewsCard from '../newsCard/NewsCard';

class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = {news: null, pageNum: 1, loadedAll:false};
    this.handleScroll = this.handleScroll.bind(this);
  }
  //render(){return (
  //);}
  //use {} about js
  render() {
    if (this.state.news) {
      return (
        <div>
          {this.renderNews()}
        </div>
      );
    } else {
      return (
        <div>
          Loading.......
        </div>
      );
    }
  }
  renderNews() {
    //traverse
    const news_list = this.state.news.map(news => {
             return (
                 <a className='list-group-item' key={news.digest} href="#">
                    <NewsCard news={news} />
                 </a>
             );
         });
    return (
          <div className="container-fluid">
              <div className="list-group">
                  {news_list}
              </div>
          </div>
      )
  }
  ComponentDidMount() {
    console.log('hhhh')
    this.loadNewsData();
    this.loadNewsData = _.debounce(this.loadNewsData, 1000);
    window.addEventListener('scroll', this.handleScroll);
  }

  loadNewsData() {
    //Request()
    if (this.state.loadedAll == true) {
      return;
    }
    const news_url = 'http://' + window.location.hostname + ':3000' +
        '/news/userId' + '/user' + '/pageNum/' + this.state.pageNum;
    console.log(news_url);
    const request = new Request(news_url, {method : 'GET', cache: false});
    fetch(request)
      .then(res => res.json())
      .then(news => {
        console.log('=====');
        console.log(news);
        if (!news || news.length == 0) {
          this.setState({loadedAll:true});
        }
          this.setState({
            news: this.state.news ? this.states.news.concat(news) : news,
            pageNum: this.state.pageNum + 1,
          });
       });
  }
  handleScroll() {
    const scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollYTop;
       if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
           console.log('Loading more news!');
           this.loadNewsData();
       }
  }
}

export default NewsPanel;
