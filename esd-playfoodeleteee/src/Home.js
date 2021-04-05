import React from 'react';
import './App.css';
import Row from './Row';
import requests from './request';
import Banner from './Banner';
import {useState, useEffect} from 'react';

function Home() {

  return (
    <div className="App">
      {/* <MyWonderfulComponent/> */}

    <Banner/>
      
      <Row title="Top Rated Games" 
      fetchURL={requests.fetchTopRatedGames}
      isLargeRow={true}
      />
      <Row title="Action" fetchURL={requests.fetchAction}/>
      <Row title="Indie" fetchURL={requests.fetchIndie}/>
      <Row title="Adventure" fetchURL={requests.fetchAdventure}/>
      <Row title="RPG" fetchURL={requests.fetchRPG}/>
      <Row title="Strategy" fetchURL={requests.fetchStrategy}/>
      <Row title="Shooter" fetchURL={requests.fetchShooter}/>
      <Row title="Casual" fetchURL={requests.fetchCasual}/>
      <Row title="Simulation" fetchURL={requests.fetchSimulation}/>
      <Row title="Puzzle" fetchURL={requests.fetchPuzzle}/>
      <Row title="Platformer" fetchURL={requests.fetchPlatformer}/>
      <Row title="Racing" fetchURL={requests.fetchRacing}/>
      <Row title="Sports" fetchURL={requests.fetchSports}/>
      <Row title="Massively Multiplayer" fetchURL={requests.fetchMassivelyMultiplayer}/>
      <Row title="Fighting" fetchURL={requests.fetchFighting}/>
      <Row title="Family" fetchURL={requests.fetchFamily}/>
      <Row title="Board Games" fetchURL={requests.fetchBoardGames}/>
      <Row title="Educational" fetchURL={requests.fetchEducational}/>
      <Row title="Card" fetchURL={requests.fetchCard}/>

    </div>
  );
}

export default Home;
