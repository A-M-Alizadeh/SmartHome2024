import {Grid, Typography } from "@mui/material";
import React from "react";
import StyledButton from "../components/button/Button";
import Wrapper from "../components/wrapper/Wrapper";
import { useNavigate } from "react-router-dom";


const Home = () => {

  const navigate = useNavigate();

  return (

    <Wrapper justifyItems={'center'} alignItems={"center"} alignContent={'flex-start'} justifyContent={'center'}>
      <Grid item mb={4} mt={18} justifyContent={'center'} alignItems={'center'} textAlign={'center'}>
        <Typography sx={{fontSize: {xs: "1.1rem",sm:"1.5rem", md: "1.7rem",lg: "2.5rem"}, color:'#fff'}} component={'h1'}>WELCOME TO AMI-DASHBOARD</Typography>
      </Grid>
      <Grid item container alignContent={'center'}  justifyContent={'center'} spacing={1.2}>
        <Grid item sx={{ backgroundColor:'transparent'}} xs={10} sm={8} md={3} lg={2}>
          <StyledButton onClick={()=>{navigate('/login')}} variant='register' buttons="buttons">Login</StyledButton>
        </Grid>
        <Grid item sx={{ backgroundColor:'transparent'}} xs={10} sm={8} md={3} lg={2}>
        <StyledButton onClick={()=>{navigate('/signup')}} variant='register' buttons="buttons">Signup</StyledButton>
        </Grid>
      </Grid>
    </Wrapper>
   
  );
};

export default Home;

