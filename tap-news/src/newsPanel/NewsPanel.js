import React from 'react';
import './NewsPanel.css';
import _ from 'lodash';
import NewsCard from '../newsCard/NewsCard';
class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = {news : null};
    this.handleScroll = this.handleScroll.bind(this);
  }
  //render(){return (
  //);}
  //use {} about js
  render() {
    if (this.state.news) {
      return (
        <div>
          {this.renderNews()};
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
    const new_list = this.state.news.map(news => {
      return(
        <a className = 'list-group-item' key={news.digest} href="#">
        //bind to subCompents
          <NewsCard news = {news}/>
        </a>
      );
    });
  }
  ComponentDidMount() {
    this.loadNewsData();
    this.loadNewsData = _.debounce(this.loadNewsData, 1000);
    window.addEventListener('scroll', this.handleScroll);
  }

  loadNewsData() {
    //Request()
    const news_url = 'http://' + window.location.hostname + ':3000/news';
    const request = new Request(news_url, {method : 'GET', cache: false});
    fetch(request)
      .then(res => res.json())
      .then(news => {
          this.setState({
            news: this.state.news ? this.states.news.concat(news) : news,
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
