import { Grid } from "@mui/material";
import React from "react";
import FacebookIcon from "@mui/icons-material/Facebook";
import WhatsAppIcon from "@mui/icons-material/WhatsApp";
import TelegramIcon from "@mui/icons-material/Telegram";
import XIcon from "@mui/icons-material/X";
import InstagramIcon from "@mui/icons-material/Instagram";
import GoogleIcon from "@mui/icons-material/Google";
const SignupIcons = () => {
  return (
    <Grid
      item
      container
      sx={{
        fontSize: { xs: "0.8rem", sm: "1rem" },
        justifyContent: "center",
        alignItems: "center",
        // marginTop:'1px'
      }}
      xs={12}
      spacing={2}
    >
      {/* <Link style={{ textDecoration:'none', color:'#1d6ee9'}}> */}
      <Grid item>
        <FacebookIcon
          sx={{
            fill: "#0072ea",
            fontSize: { xs: 17, sm: 18, md: 25 },
            marginTop: 1,
            cursor: "pointer",
          }}
        />
      </Grid>
      <Grid item>
        <WhatsAppIcon
          sx={{
            fill: "#4db10b",
            fontSize: { xs: 17, sm: 18, md: 25 },
            marginTop: 1,
            cursor: "pointer",
          }}
        />
      </Grid>
      <Grid item>
        <GoogleIcon
          sx={{
            fill: "#ff6d0b",
            fontSize: { xs: 17, sm: 18, md: 25 },
            marginTop: 1,
            cursor: "pointer",
          }}
        />
      </Grid>
      <Grid item>
        <XIcon
          onClick={() => console.log("Clicked!")}
          sx={{
            fill: "#d3d3d3",
            fontSize: { xs: 17, sm: 18, md: 25 },
            marginTop: 1,
            cursor: "pointer",
            '&:hover': {
              cursor: 'pointer',
              color:'red'
            }


          }}
        />
      </Grid>
      <Grid item>
        <TelegramIcon
          sx={{
            fill: "#34b0f8",
            fontSize: { xs: 17, sm: 18, md: 25 },
            marginTop: 1,
            cursor: "pointer",
            '&:hover': {
              cursor: 'pointer',
              color:'red'
            }
          }}
        />
      </Grid>
      <Grid item>
        <InstagramIcon
          sx={{
            fill: "#ea0089",
            fontSize: { xs: 17, sm: 18, md: 25 },
            marginTop: 1,
            cursor: "pointer",
          }}
        />
      </Grid>
      {/* </Link> */}
    </Grid>
  );
};

export default SignupIcons;
