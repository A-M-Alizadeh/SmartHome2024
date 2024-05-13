import {
  Alert,
  AppBar,
  Box,
  Button,
  Grid,
  Toolbar,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import MenuIcon from "@mui/icons-material/Menu";
import IconButton from "@mui/material/IconButton";
import NotificationsActiveSharpIcon from "@mui/icons-material/NotificationsActiveSharp";
const drawerWidth = 250;

const Header = ({ isClosing, setMobileOpen, mobileOpen }) => {
  const [isAlertOpened, setIsAlertOpend] = useState(false);

  const handleDrawerToggle = () => {
    if (!isClosing) {
      setMobileOpen(!mobileOpen);
    }
  };

  return (
    <AppBar
      style={{ backgroundColor: "#0047b3" }}
      position="fixed"
      sx={{
        width: { sm: `calc(100% - ${drawerWidth}px)` },
        ml: { sm: `${drawerWidth}px` },
      }}
    >
      <Toolbar sx={{ justifyContent: { xs: "flex-end" } }}>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={handleDrawerToggle}
          sx={{ mr: 2, display: { sm: "none" } }}
        >
          <MenuIcon />
        </IconButton>
        {isAlertOpened ? (
          <Alert
            severity="success"
            color="warning"
            sx={{
              width: { xs: "85%", lg: "95%" },
              height: "150px",
              position: "absolute",
              top: "10px",
              right: { xs: "45px", lg: "60px" },
              // backgroundColor:'#203342',
              // boxShadow:'1px 2px 3px rgba(255,255,255,0.5)'
            }}
            action={
              <Button
                onClick={() => setIsAlertOpend(!isAlertOpened)}
                color="inherit"
                size="small"
              >
                UNDO
              </Button>
            }
          >
            <Grid item>This Alert uses a Button component for its action.</Grid>
            <Grid item>This Alert uses a Button component for its action.</Grid>
          </Alert>
        ) : (
          ""
        )}
        <NotificationsActiveSharpIcon
          onClick={() => {
            setIsAlertOpend(!isAlertOpened);
          }}
          sx={{
            justifyContent: "flex-end",
            cursor: "pointer",
            "&:hover": {
              color: "#f5b869",
              transition: "all 1s ease",
            },
          }}
        />
      </Toolbar>
    </AppBar>
  );
};

export default Header;
