import 'materialize-css/dist/css/materialize.min.css';
import NewsPanel from '../newsPanel/NewsPanel';
import React from 'react';
import './App.css';
import logo from './image.png';
class App extends React.Component {
  render() {
    return(
      <div>
        <img className = 'logo' src = {logo} alt = 'logo'/>
        <div className = 'container'>
          <NewsPanel />
        </div>
      </div>
    );
  }

}
//use default, so we can use import a instead of {a}
export default App;
