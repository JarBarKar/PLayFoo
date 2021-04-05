import React from 'react';
import "./Message.css";
import Button from 'react-bootstrap/Button';
import {useState, useEffect} from 'react';
import axios from 'axios';
import { MdAccountCircle } from 'react-icons/md';

function Message( {match} ) {

    const user = localStorage.getItem("user");
    const room_id = localStorage.getItem('roomid');

    const [message, setMessage] = useState([]);

    async function GetMessages() {
        let data = {room_id: room_id}
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://localhost:5003/message',
              data: data
            })
          if (onSubmit.status == 200){
              console.log(onSubmit)
              setMessage(onSubmit.data.data.messages);
            // alert("You have successfully created room " + data.roomid);
          }
          return onSubmit.status
        }
        catch (err) {
          console.log(err);
        }
      }

    console.log(message)

    useEffect(() => {
        const interval = setInterval(() => {
            GetMessages()
             console.log('Logs every minute');
        }, 1000 );
      
        return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
      }, [])

    return (
        <div className='convo'>
            {Array.from(message).map((_, index) => (
                <div className='content' style={{width:'100%'}}>
                    <div>
                        <div style={{float: 'left', width: '50%', fontSize:'18px'}}>
                            <MdAccountCircle size={30}/>&nbsp;
                            {message[index].user_id} &nbsp;
                        </div>
                        <div style={{float: 'right', width: '50%', fontSize:'12px'}}>
                            {message[index].timestamp}
                        </div>
                    </div>

                    <div style={{float:'left', width: '100%', padding: '5px', fontSize:'15px'}}>
                        {message[index].content}
                    </div>
                </div>
            ))}

            {/* <div>
                <Button variant="primary" onClick={() => GetMessages()}>Primary</Button>
            </div> */}

        </div> 
    )
}
export default Message
