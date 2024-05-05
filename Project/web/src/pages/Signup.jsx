import React, { useState } from "react";
import { StyledInput } from "../components/input/Input.styles";
import { Grid, Typography } from "@mui/material";
import RegisterContainer from "../components/registerContainer/RegisterContainer";
import Wrapper from "../components/wrapper/Wrapper";
import { StyledButton } from "../components/button/Button.styles";
import { Link, useNavigate } from "react-router-dom";
import SignupIcons from "../components/icons/SignupIcons";
import { StyledLink } from "../components/link/Link.styles";
import {catalogUrl, catalogPort} from "../generalConfig";

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
    username: "",
    first_name: "newname",
    last_name: "newFamilyName",
    email: "newuser@gmail.com",
    phone: "123-456-789",
    password: "123456789",
    confirmPassword: "123456789",
    houseTitle: "HOUSE TITLE NEW #1",
    houseAddress: "Corso Vittorio Emanuele II, 11, 00186 Roma RM, Italy",
  });

  const handleInput = (event) => {
    const newObject = { ...values, [event.target.name]: event.target.value };
    setValues(newObject);
  };

  const hanldeSubmit = () => {
    fetch(`${catalogUrl}${catalogPort}/auth/fullRegister`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user:{
          username: values.username, 
          password: values.password,
          email: values.email,
          first_name: values.first_name,
          last_name: values.last_name,
          phone: values.phone,
        },
        house:{
          title: values.houseTitle,
          address: values.houseAddress
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
              value={values.username}
              placeholder="Username"
              type="text"
              name="username"
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
              value={values.first_name}
              placeholder="first Name"
              type="text"
              name="first_name"
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
              value={values.last_name}
              placeholder="Last Name"
              type="text"
              name="last_name"
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
              value={values.email}
              placeholder="Email"
              type="text"
              name="email"
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
              value={values.phone}
              placeholder="Phone"
              type="text"
              name="phone"
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
              value={values.houseTitle}
              placeholder="House Title"
              type="text"
              name="houseTitle"
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
              value={values.houseAddress}
              placeholder="House Address"
              type="text"
              name="houseAddress"
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
