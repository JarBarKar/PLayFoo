import {useState, useEffect} from 'react';
import axios from './axios';
import "./Row.css";

import { BrowserRouter as Router, Route, Link, NavLink, Switch} from "react-router-dom";


function Row({title, fetchURL, isLargeRow}) {

    const [games, setGame] = useState([]);
   
    useEffect(async () => {
        console.log('running');
        const result = await axios(fetchURL,
      );
      console.log(fetchURL);
      setGame(result.data);
      return result;
    }, [fetchURL]);

    console.log(games);

    function refreshPage() {
      setTimeout(()=>{
          window.location.reload(false);
      }, 500);
      console.log('page to reload')
    }

    function printDescription() {
      try {
        var description = games[1].abc;
        if (description == "undefined") {
          var description = '';
        }
        return description
      } catch (err) {
        console.error(err.message);
      } 
    }
   
    return (
      <Router>
        <div className="row">

          <div style={{marginLeft:'30px',width:'100%', }}>
            <h2 key={title}>
              <Link to={`/genre/${title}`} onClick={refreshPage} style={{color:'orange'}}>
                <b>{title}</b>
              </Link>
            </h2>
          </div>

          <div style={{marginLeft:'30px', width:'100%', fontFamily: 'Arial Narrow, sans-serif'}}>
            <h5>
                {/* {games[1].abc} */}
                {printDescription()}
            </h5>
          </div>

          <div className="row_posters">
            {games.map(game =>(
                <Link to={{
                  pathname: `/game/${game.id}`,
                  state: game
                }} key={game.id} onClick={refreshPage}>
                  <img 
                    key={game.id}
                    className={`row_poster ${isLargeRow && "row_posterLarge"}`}
                    src={game.background_image}/>
                    <h6 style={{color:'white'}}>{game.name}</h6>
                </Link>
            ))}
          </div>
        </div>
      </Router>
    )
  }

export default Row
