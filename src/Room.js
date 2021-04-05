import React from 'react';
import "./Room.css";
import Button from 'react-bootstrap/Button';
import {useState, useEffect} from 'react';
import Message from './Message';
import { FaMicrophone } from 'react-icons/fa';
import {AiFillSetting, AiFillVideoCamera, AiOutlineNodeIndex} from 'react-icons/ai';
import axios from 'axios';
import { useHistory } from 'react-router-dom';


function Room( {match} ) {

    const history = useHistory();
    const [value, setValue] = useState("");
    const room_id = match.params.roomid;
    localStorage.setItem('roomid', room_id);

    const handleChange = e => {
        setValue(e.target.value);
    };

    async function handleKeypress(e) {
        var key = e.which;
      if (key === 13) {
        handleSubmit(e);
      }
    };

    async function handleSubmit(e){
        e.preventDefault();
        setValue("");
        // alert(value);

        let data = {room_id: room_id, user_id: user , content: value}
        console.log(data)
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://localhost:8000/send_message',
              data: data
            })
        //   if (onSubmit.status == 201){
        //     history.push(`/home`);
        //     // alert("You have successfully created room " + data.roomid);
        //   }
          return onSubmit.status
        }
        catch (err) {
          console.log(err);
        }
        // or you can send data to backend
    };

    const user = localStorage.getItem("user");
    const gameid = localStorage.getItem("gameid");

    const [rooms, setRooms] = useState([]);
   
    useEffect(async () => {
        const result = await axios("http://localhost:5001/room/detail/" + room_id
      );
      setRooms(result.data.data);
      return result;
    }, []);

    // console.log(rooms.members)

    async function LeaveRoom() {
        let data = {room_id: room_id, user_id: user }
        console.log(data)
        try{
          const onSubmit =
            await axios({
              method: 'delete',
              url: 'http://localhost:8000/leave_room',
              data: data
            })
          if (onSubmit.status == 201){
            history.push(`/home`);
            // alert("You have successfully created room " + data.roomid);
          }
          return onSubmit.status
        }
        catch (err) {
          console.log(err);
        }
      }

    function getMembers() {
        try {
            var members_list = [];
            if (rooms.members != "undefined") {
                members_list = rooms.members;
            }
            return members_list
        } catch (err) {
            console.error(err.message);
        } 
    }

    return (
        <div className="row">
            <div className="block" style={{height: '100px'}}></div>
                <div className="float-container">
                    <div class="float-child">
                        <div class="green" style={{float:'left'}}>
                            <div className='title'>
                                <div style={{display: 'inline-flex', position: 'relative', width: '80%'}}>
                                    <h4>
                                    {rooms.room_name}
                                    </h4>
                                </div>
                            
                                <div style={{ display: 'inline-flex', position: 'relative', float: 'right'}}>
                                    <Button variant="danger" onClick={LeaveRoom}>Leave</Button>
                                </div>
                            </div>
                            <div className='messages'>
                                <Message/>
                            </div>
                            
                        </div>
                    </div>
                    
                    <div class="float-child">
                        <div className="blue" style={{float: 'right', backgroundColor: '#555555'}}>
                            <div>
                                <h5>Members</h5>
                            </div>

                            {/* {Array.from(getMembers()).map((_, index) => (
                                <div className='friend'>
                                    {getMembers()[index]}
                                </div> */}
                            {/* ))} */}

                                <div className='friend'>
                                    {getMembers()}
                                </div>

                        </div>
                    </div>

                    <div class="float-child">
                        <div style={{display: 'inline-flex', position: 'relative', width: '80%'}}>
                            <input 
                                className='bottom' 
                                type="text" 
                                style={{width:'90%'}} 
                                onKeyPress={handleKeypress}  
                                value={value}
                                onChange={handleChange}
                            ></input>
                            <Button variant="light" 
                                type='submit' 
                                style={{width:'10%'}} 
                                onClick={handleSubmit} 
                                // ref={node => (btn = node)}
                            >Send</Button>
                        </div>

                        <div style={{display: 'inline-flex', position: 'relative', width: '10%', height: '50px'}}>
                            <h5 style={{alignContent: 'center', margin: 'auto'}}>#{user}</h5>
                        </div>

                        <div style={{display: 'inline-flex', position: 'relative', width: '10%', float: 'right', height: '50px'}}>
                            <div style={{alignContent: 'center', margin: 'auto'}}>
                                <FaMicrophone style={{margin:'5px'}} size={25}/>
                                <AiFillVideoCamera style={{margin:'5px'}} size={25}/>
                                <AiFillSetting style={{margin:'5px'}} size={25}/>
                            </div>
                        </div>

                    </div>
                </div>
            <div className="block" style={{height: '42px'}}></div>
        </div>

    )
}

export default Room