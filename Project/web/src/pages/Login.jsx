import React, { useState } from "react";
import Wrapper from "../components/wrapper/Wrapper";
import { Grid, Paper, Typography } from "@mui/material";
import RegisterContainer from "../components/registerContainer/RegisterContainer";
import { StyledInput } from "../components/input/Input.styles";
import { StyledButton } from "../components/button/Button.styles";
import { Link, useNavigate } from "react-router-dom";
import { StyledLink } from "../components/link/Link.styles";
import {catalogUrl, catalogPort} from "../generalConfig";

const Login = () => {
  const [emailBorderColor, setEmailBorderColor] = useState(true);
  const [passwordBorderColor, setPasswordBorderColor] = useState(true);
  const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,6}$/;
  const password_pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}$/;

  const [values, setValues] = useState({
    email: "newAuthUsername",
    password: "123456789",
  });

  const handleInput = (event) => {
    const newObject = { ...values, [event.target.name]: event.target.value };
    setValues(newObject);
  };

  const navigate = useNavigate();
  const handleSubmit = () => {

    fetch(`${catalogUrl}${catalogPort}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({username: values.email, password: values.password}),
    })
      .then((res) => res.json())
      .then((data) => {
        localStorage.setItem("userData", JSON.stringify(data));
        console.log(data)
        navigate("/dashboard");
      }).catch((error) => {
        console.log(error);
      });
    
  };

  return (
    <Wrapper alignContent={"center"} justifyContent={"center"}>
      <RegisterContainer
        backgroundColor={"red"}
        sx={{
          width: { xs: 320, sm: 350, md: 380 },
          height: { xs: 360, sm: 390, md: 430 },
        }}
        
      >
        <Grid item sx={{ marginTop: { xs: 2, sm: 3, md: 5 } }}>
          <Typography variant="h4" component={"h1"} style={{ color: "#fff" }}>
            Login
          </Typography>
        </Grid>
          <Grid
            item
            container
            alignContent={"center"}
            spacing={2}
            sx={{ marginTop: { xs: 3, sm: 4, md: 5 }, textAlign: "center" }}
          >
            <Grid item xs={12}>
              <StyledInput
                // onChange={(e) => setEmail(e.target.value)}
                style={
                  emailBorderColor
                    ? { border: "1px solid #dddddd" }
                    : { border: "1px solid red" }
                }
                onChange={handleInput}
                placeholder="Email"
                value={values.email}
                type="email"
                name="email"
              ></StyledInput>
            </Grid>
            <Grid item xs={12}>
              <StyledInput
                // onChange={(e) => setPassword(e.target.value)}
                style={
                  passwordBorderColor
                    ? { border: "1px solid #dddddd" }
                    : { border: "1px solid red" }
                }
                onChange={handleInput}
                placeholder="Password"
                value={values.password}
                type="password"
                name="password"
              ></StyledInput>
            </Grid>
          </Grid>
          <Grid item xs={11} sx={{ marginTop: { xs: 3, sm: 4, md: 5 }, textAlign:'center' }}>
            <StyledButton
              type="submit"
              onClick={handleSubmit}
              variant="radius"
              buttons="buttons"
            >
              Login
            </StyledButton>
          </Grid>
        <Grid
          item
          container
          sx={{ marginTop: { xs: 2, sm: 3, md: 4 } }}
          spacing={1}
          justifyContent={"space-around"}
        >
          <Grid item sx={{ fontSize: { xs: "0.8rem", sm: "1rem" } }}>
            <StyledLink to="/signup" variant="linkhover">
              Dont have an account!
            </StyledLink>
          </Grid>
          <Grid item sx={{ fontSize: { xs: "0.8rem", sm: "1rem" } }}>
            <StyledLink to="/forget-password" variant="linkhover">
              Forget Password!
            </StyledLink>
          </Grid>
        </Grid>
      </RegisterContainer>
    </Wrapper>
  );
};

export default Login;
