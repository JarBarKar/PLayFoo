import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./Login.css";
import axios from './axios';
import { useHistory } from 'react-router-dom';
import { useForm } from "react-hook-form";

import { BrowserRouter as Router, Route, Link, NavLink, Switch} from "react-router-dom";

export default function Login() {
  const [user, setUser] = useState([]);
  const [password, setPassword] = useState([]);
  const history = useHistory();

  function validateForm() {
    return user.length > 0 && password.length > 0;
  }

  const { register, handleSubmit } = useForm({
    defaultValues: {
      user_id : user
    }
  });

  async function getData() {
    localStorage.setItem("user", user);
    let data = {user_id: user}
    console.log(data)
    try{
      const onSubmit =
        await axios({
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
            mode: 'no-cors',
            method: 'post',
            url: 'http://localhost:5000/userid',
            data: data
        })
      if (onSubmit.status == 200){
        // console.log(onSubmit.data.data);
        // console.log(password)
        if (onSubmit.data.data.password == password) {
          history.push(`/home`);
        } else {
          alert("Please re-enter your credentials");
        }
      }
      return onSubmit.status
    }
    catch (err) {
      console.log(err);
    }
  }



  return (
    <body>
        <div className='loginbox' style={{height: '100%', width: '100%',}}>
          {/* <div className="block"></div> */}
          <div className='image'>
            <img
              src="https://playfoo-image.s3.amazonaws.com/PLayFoo.png"
              style={{marginLeft:'auto', marginRight:'auto', display:'block'}}
            />
          </div>
            <div className="Login">
              <Form onSubmit={handleSubmit(getData)}>
                  <Form.Group size="lg" controlId="email">
                  <Form.Label>User</Form.Label>
                  <Form.Control
                      type="text"
                      value={user}
                      onChange={(e) => setUser(e.target.value)}
                      ref={register}
                  />
                  </Form.Group>
                  <Form.Group size="lg" controlId="password">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      ref={register}
                  />
                  </Form.Group>
                  <Button block size="lg" type="submit" disabled={!validateForm()}>
                  Login
                  </Button>
                  &nbsp;
                  <Link to={'/'} style={{color:'white'}}>Do not have an account? Sign up here now!</Link>
              </Form>
          </div>
      </div>
    </body>
  );
}