import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';
import axios from './axios';
import {useState, useEffect} from 'react';
import { useHistory } from 'react-router-dom';

function Joinroom(props) {
  console.log("joinroom is running now")

  const history = useHistory();
  const user_id = localStorage.getItem("user");
  // console.log(user_id);
  const gameid = localStorage.getItem("gameid");
  const roomid= localStorage.getItem("roomid");

  const [rooms, setRooms] = useState([]);
   
  useEffect(async () => {
      console.log('running');
      const result = await axios("http://localhost:5001/room/" + gameid
    );
    // console.log(result)
    setRooms(result.data.data.rooms);
    return result;
  }, []);

  console.log(rooms);

  async function SelectRoom(data) {
    let fdata = {room_id: data.room_id, room_name: data.room_name, user_id: user_id};
    console.log(data.room_id)
    try{
      const onSubmit =
        await axios({
          method: 'post',
          url: 'http://localhost:5001/room/' + data.room_id,
          data: fdata
        })
        // console.log(onSubmit)
      if (onSubmit.status == 201){
        // console.log(onSubmit)
        const join_message = fdata.user_id + " has joined room";
        let data = {room_id: fdata.room_id, user_id: fdata.user_id , content: join_message}
        try{
            const newuser =
              await axios({
                method: 'post',
                url: 'http://localhost:5103/message/send',
                data: data
                })
            }
            catch (err) {
              console.log(err);
            }
        history.push(`/room/` + data.room_id);
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
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter"  style={{color: 'white'}}>
          ROOMS
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
          <Table responsive>
              <thead>
                  <tr style={{color: 'white'}}> 
                      <th>Room ID #</th>
                      <th>Room Name</th>
                      <th>Owner</th>
                      <th>Capacity</th>
                  </tr>
              </thead>
              <tbody>
                    {Array.from(rooms).map((_, index) => ( 
                      // console.log("loop")
                      <tr style={{color: 'white'}}>
                          {rooms[index].room_id}
                          <td>{rooms[index].room_name}</td>
                          <td>{rooms[index].host_id}</td>
                          <td>{rooms[index].capacity}
                          <Button 
                            type="submit" 
                            variant="secondary" 
                            style={{float: "right",}} 
                            onClick={() => SelectRoom(rooms[index])}
                          >Join</Button>
                          </td>
                      </tr>
                  ))}
              </tbody>
          </Table>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  );
}

export default Joinroom