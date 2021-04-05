import React from 'react';
import './App.css';
import Row from './Row';
import requests from './request';
import Banner from './Banner';
import Nav from './Nav';
import Home from './Home';
import Genre from './Genre';
import Game from './Game';
import Room from './Room';
import Login from './Login';

import { BrowserRouter as Router, Route, Link, NavLink, Switch} from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path ="/" exact component={Login}/>
          <div>
            <Nav/>
              <Route path="/home" exact component={Home}/>
              <Route path="/genre/:name" component={Genre}/>
              <Route path="/game/:id" component={Game}/>
              <Route path="/room/:roomid" component={Room}/>
          </div>
          
        </Switch>
      </div>

    </Router>
    
  );
}

export default App;
