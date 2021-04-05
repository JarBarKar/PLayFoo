import React, { useEffect, useState } from 'react'
import './Nav.css';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
import { BrowserRouter as Router, Route, Link, NavLink, Switch} from "react-router-dom";

function Nav() {
    const [show, handleShow] = useState(false);
    
    useEffect(() => {
        window.addEventListener("scroll", () => {
            if (window.scrollY >100 ) {
                handleShow(true);
            } else handleShow(false);
        });
        return () => {
            window.removeEventListener("scroll");
        };
    }, []);

    async function getData(){
        localStorage.setItem('user', "");
        localStorage.setItem('roomid', "");
        localStorage.setItem('password', "");
        localStorage.setItem('gameid', "");
    }

    function refreshPage() {
        setTimeout(()=>{
            window.location.reload(false);
        }, 500);
        console.log('page to reload')
    }

    return (
        <div className={`nav ${show && "nav_black"}`}>
            <Link to={`/home`} onClick={refreshPage}>
                <img
                    className="nav_logo"
                    src="https://playfoo-image.s3.amazonaws.com/PLayFoo.png"
                    // alt="Netflix Logo"
                />
            </Link>
            <DropdownButton 
            id="dropdown-basic-button" 
            className="nav_avatar"
            // title = "Dropdown button"
            >
                <Dropdown.Item href="#/action-1">My Profile</Dropdown.Item>
                <Dropdown.Item >Settings</Dropdown.Item>
                <Dropdown.Item href="/" onClick={getData}>Logout</Dropdown.Item>
            </DropdownButton>

            {/* <img
                className="nav_avatar"
                src="https://upload.wikimedia.org/wikipedia/commons/0/0b/Netflix-avatar.png"
                alt="Netflix Logo"
            /> */}

        </div>
    )
}

export default Nav
