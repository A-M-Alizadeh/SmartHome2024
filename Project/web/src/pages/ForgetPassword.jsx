import React, { useState } from 'react'
import Wrapper from '../components/wrapper/Wrapper'
import RegisterContainer from '../components/registerContainer/RegisterContainer'
import { Grid, Typography } from '@mui/material'
import { StyledButton } from '../components/button/Button.styles'
import { StyledInput } from '../components/input/Input.styles'
import { Link, useNavigate } from 'react-router-dom'
import { StyledLink } from '../components/link/Link.styles'

const ForgetPassword = () => {

  const [email, setEmail] = useState("");
  const [borderColor, setBorderColor] = useState(true);
  const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,6}$/;
  const navigate = useNavigate();

  const handleSubmit = ()=>{
    console.log('Forget Password Submitted!');

    if (email === "" && !email_pattern.test(email)) {
      setBorderColor(false);
      console.log('if')
    } else {
      setBorderColor(true);
      console.log('if else')
    }
  }


  return (
    <Wrapper alignContent={"center"} justifyContent={"center"}>
    <RegisterContainer sx={{ width: {xs:320, sm:350, md: 380 }, height: {xs:260,sm:280, md: 300 } }}>
      <Grid item sx={{ marginTop: { xs: 2, md: 3 } }}>
        <Typography variant="h5" component={"h1"} style={{ color: "#fff" }}>
          Forget Password
        </Typography>
      </Grid>
      <Grid
        item
        container
        alignContent={"center"}
        spacing={2}
        sx={{ marginTop: { xs: 2, md: 3 }, textAlign: "center" }}
      >
        <Grid item xs={12}>
          <StyledInput  style={
              borderColor
                ? { border: "1px solid #dddddd" }
                : { border: "1px solid red" }
            } onChange={(e)=>setEmail(e.target.value)} value={email} placeholder="Email" type="email" />
        </Grid>
      </Grid>
      <Grid item xs={11} sx={{ marginTop: { xs: 2, md: 3 } }}>
        <StyledButton onClick={handleSubmit} variant="radius" buttons="buttons">Update Password</StyledButton>
      </Grid>
      <Grid
        item
        container
        sx={{marginTop: { xs: 2, sm: 3, md: 4 } }}
        spacing={1}
        justifyContent={'space-around'}
      >
        <Grid item sx={{fontSize:{xs:'0.8rem',sm:'1rem'}}}>
          <StyledLink to='/login' variant="linkhover">Back to Login!</StyledLink>
        </Grid>
      </Grid> 
    </RegisterContainer>
  </Wrapper>
  )
}

export default ForgetPassword