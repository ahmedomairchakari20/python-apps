import '../styles/forget.css'
import React from 'react'
import { useState } from 'react'
import { faUnlockAlt } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import axios from "axios"
import { useNavigate } from 'react-router-dom';

export default function ForgetPassword() {
  
  const [email, setEmail] = useState("")
  const Navigate = useNavigate()
  async function emailhandler(e) {
    e.preventDefault()

    try {
      const response = await axios.post("http://18.205.162.184:8000/forgetPassword", {
        email: email,
      })
      console.log(response.data.email)
      if(response.data.msg=="user exist"){
        Navigate('/resetPassword/'+email)
      }


    } catch (error) {
      console.error(error)
    }
  }
  return (
    <>
    <div className="wrapper">
      <div className="containerforget">
        <div className="forgeticon">
        <FontAwesomeIcon icon={faUnlockAlt}  className='forgeticon' size='2xl' style={{color: "#ffffff",}} />
        </div>
          <div className="title">
            <p style={{color:"#ffffff",}}>Forget Password?</p>
            <p style={{color:"#ffffff",}}>Please enter your registeration email address below.</p>
          </div>
          <form onSubmit={emailhandler}>
            <div className="field">
               <input type={"text"}
                onChange={(e) => setEmail(e.target.value)}
                value={email}
                placeholder="Enter email"
                required/>
            </div>
            <div className="field2">
               <input type={"submit"} value="Send Reset Instruction"/>
            </div>
         </form>

      </div>
    </div>
    </>
  )
}
