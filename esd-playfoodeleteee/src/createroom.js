import React from 'react';
import Modal from 'react-bootstrap/Modal';
import { useForm } from "react-hook-form";
import axios from './axios';
import { useHistory } from 'react-router-dom';
import './createroom.css';

function Createroom(props) {

  const history = useHistory();
  const user = localStorage.getItem('user');
  const gameid = localStorage.getItem('gameid');
  console.log(gameid)

  const { register, handleSubmit } = useForm({
    defaultValues: {
      game_id: gameid,
      host_id: user,
      room_name: "",
      capacity: ""
    }
  });

  async function getData(data) {
    try{
      const onSubmit =
        await axios({
          method: 'post',
          url: 'http://localhost:5001/room',
          data: data
        })
      if (onSubmit.status == 201){
        // console.log(onSubmit);
        history.push(`/room/${onSubmit.data.data.room_id}`);
        // alert("You have successfully created room " + data.roomid);
      }
      return onSubmit.status
    }
    catch (err) {
      console.log(err);
    }
  }

  return (
    <Modal
      {...props}
      size="md"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter" style={{color: 'white'}}>
          CREATE ROOM
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>

        <form onSubmit={handleSubmit(getData)}>
          {/* <div>
            <h4 style={{color: 'white', float:'left', width:'35%'}}>Room ID #</h4>
            <input type="number" readOnly name="game_id" ref={register} placeholder="Room Id #" style={{marginLeft: '20%'}}/>
          </div> */}
          &nbsp;
          <div>
            <h4 style={{color: 'white', float:'left', width:'35%'}}>Owner</h4>
            <input readOnly name="host_id" ref={register} placeholder="Owner" style={{marginLeft: '20%'}}/>
          </div>
          &nbsp;
          <div>
            <h4 style={{color: 'white', float:'left', width:'35%'}}>Room Name</h4>
            <input name="room_name" ref={register} placeholder="Enter Room Name here" style={{marginLeft: '20%'}}/>
          </div>
          &nbsp;
          <div>
            <h4 style={{color: 'white', float:'left', width:'35%'}}>Capacity</h4>
              <select name="capacity" ref={register} style={{marginLeft: '20%'}} >
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
              </select>
          </div>
          &nbsp;
          
          <div>
            <input style={{float:'left', width:'35%'}} type="submit" value="Create Room" />
          </div>
          
        </form>
        
      </Modal.Body>
    </Modal>
  );
}

export default Createroom