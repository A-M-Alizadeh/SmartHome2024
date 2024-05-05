import React, { useState } from "react";
import { StyledInput } from "../components/input/Input.styles";
import { Grid, Typography } from "@mui/material";
import RegisterContainer from "../components/registerContainer/RegisterContainer";
import Wrapper from "../components/wrapper/Wrapper";
import { StyledButton } from "../components/button/Button.styles";
import { Link, useNavigate } from "react-router-dom";
import SignupIcons from "../components/icons/SignupIcons";
import { StyledLink } from "../components/link/Link.styles";

const Signup = () => {
  // const [email, setEmail] = useState("");
  // const [password, setPassword] = useState("");
  // const [rePassword, setRePassword] = useState("")
  const navigate = useNavigate();

  const [emailBorderColor, setEmailBorderColor] = useState(true);
  const [passwordBorderColor, setPasswordBorderColor] = useState(true);
  const [confirmpassBorderColor, setConfirmpassBorderColor] = useState(true);

  const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,6}$/;
  const password_pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}$/;
  const confirmPassword_pattern =
    /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}$/;

  const [values, setValues] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleInput = (event) => {
    const newObject = { ...values, [event.target.name]: event.target.value };
    setValues(newObject);
  };

  const hanldeSubmit = () => {
    fetch("http://localhost:8082/fullRegister", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user:{
          username: 'newUser1', 
          password: '123456789',
          email: "newuser@gmail.com",
          first_name: "newname",
          last_name: "newFamilyName",
          phone: "123-456-789",
        },
        house:{
          title: "New House 1",
          address: "New House 1 Address.sq 1 block 1",
        },
        sensors:[
          {
            type: "TEMPERATURE",
          },
          {
            type : "HUMIDITY"
          },{
            type: "AIR_CONDITIONER"
          }
        ]
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
          navigate("/login");
      }).catch((error) => {
        console.log(error);
      });
  };

  return (
    <Wrapper alignContent={"center"} justifyContent={"center"}>
      <RegisterContainer
        sx={{
          width: { xs: 330, sm: 360, md: 400 },
          // height: { xs: 420, sm: 450, md: 500 },
        }}
      >
        <Grid item sx={{ marginTop: { xs: 2, sm: 3, md: 5 } }}>
          <Typography variant="h4" component={"h1"} style={{ color: "#fff" }}>
            Signup
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
              onChange={handleInput}
              value={values.email}
              placeholder="Email"
              type="email"
              name="email"
              style={
                emailBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>
          <Grid item xs={12}>
            <StyledInput
              onChange={handleInput}
              value={values.password}
              placeholder="Password"
              type="password"
              name="password"
              style={
                passwordBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>
          <Grid item xs={12}>
            <StyledInput
              onChange={handleInput}
              value={values.confirmPassword}
              placeholder="Confirm Password"
              type="password"
              name="confirmPassword"
              style={
                confirmpassBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>








          <Grid item xs={12}>
            <StyledInput
              onChange={handleInput}
              value={values.confirmPassword}
              placeholder="Username"
              type="password"
              name="confirmPassword"
              style={
                confirmpassBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>
          <Grid item xs={12}>
            <StyledInput
              onChange={handleInput}
              value={values.confirmPassword}
              placeholder="First Name"
              type="password"
              name="confirmPassword"
              style={
                confirmpassBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>
          <Grid item xs={12}>
            <StyledInput
              onChange={handleInput}
              value={values.confirmPassword}
              placeholder="Last Name"
              type="password"
              name="confirmPassword"
              style={
                confirmpassBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>
          <Grid item xs={12}>
            <StyledInput
              onChange={handleInput}
              value={values.confirmPassword}
              placeholder="Phone"
              type="password"
              name="confirmPassword"
              style={
                confirmpassBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>
          <Grid item xs={12}>
            <StyledInput
              onChange={handleInput}
              value={values.confirmPassword}
              placeholder="House Title"
              type="password"
              name="confirmPassword"
              style={
                confirmpassBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>
          <Grid item xs={12}>
            <StyledInput
              onChange={handleInput}
              value={values.confirmPassword}
              placeholder="House Address"
              type="password"
              name="confirmPassword"
              style={
                confirmpassBorderColor
                  ? { border: "1px solid #dddddd" }
                  : { border: "1px solid red" }
              }
            ></StyledInput>
          </Grid>















        </Grid>
        <Grid item xs={11} sx={{ marginTop: { xs: 3, sm: 4, md: 5 } }}>
          <StyledButton
            onClick={hanldeSubmit}
            variant="radius"
            buttons="buttons"
          >
            Signup
          </StyledButton>
        </Grid>
        <Grid
          item
          container
          sx={{ marginTop: { xs: 0, sm: 1 } }}
          spacing={1}
          textAlign={"center"}
          // marginBotto  m={10}
        >
          <SignupIcons />
          <Grid item sx={{ fontSize: { xs: "0.8rem", sm: "1rem" } }} xs={12}>
            <StyledLink to="/login" variant="linkhover">
              Already have an account!
            </StyledLink>
          </Grid>
        </Grid>
      </RegisterContainer>
    </Wrapper>
  );
};

export default Signup;
