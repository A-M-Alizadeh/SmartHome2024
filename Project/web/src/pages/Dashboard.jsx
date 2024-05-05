import React,{useState, useEffect} from "react";
import { Box, Grid } from "@mui/material";
import Divider from "@mui/material/Divider";
import DeleteIcon from "@mui/icons-material/Delete";
import NewspaperSharpIcon from "@mui/icons-material/NewspaperSharp";
import { StyledText } from "../components/text/Text.styles";
import { useNavigate } from "react-router-dom";
// import Image from "../components/avatar/Image";

const Dashboard = () => {

  const [houses, setHouses] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    getHousesList();
  }, []);

  const getHousesList = () => {
    let userData = JSON.parse(localStorage.getItem("userData"));
    setHouses(userData.houses);
  }

  return (
    <Grid container sx={{ height: "", backgroundColor: "#353455" }}>
      <Grid container spacing={4} flex={1} height="100%">
        {houses.map((item, index) => {
          return (
            <Grid key={index} item xs={12} md={6} lg={3}>
              <Box bgcolor="#0047b3" borderRadius={2} width="100%" height="300px">
                <Grid item container sx={{ padding: 2 }}>
                  <Grid
                    item
                    container
                    sx={{
                      display: "flex",
                      alignItems: "center",
                    }}
                  >
                    <Grid item>
                      <StyledText variant="textTitle" style={{fontSize: 18}}>
                        {item.title}
                      </StyledText>
                      <Grid
                        item
                      >
                        <StyledText style={{fontSize: 12}}>{item.address}</StyledText>
                      </Grid>
                        <StyledText style={{fontSize: 8}}>{item.house_id}</StyledText>
                    </Grid>
                  </Grid>
                      <button onClick={()=>navigate('/sensor', {state: {house_id: item.house_id, house: item}})} style={{backgroundColor: 'blue', color: 'white', borderRadius: 5, padding: 5, marginTop: 5}}>View Sensors</button>
                  <Divider
                    style={{
                      backgroundColor: "#acacac",
                      width: "100%",
                      margin: "auto",
                      marginTop: 2,
                    }}
                  />
                  <Grid
                    md={12}
                    style={{marginTop: 5}}
                  >
                    {item.sensors.map((sensor, index) => {
                      return (
                        <div key={index} style={{ borderWidth: '1px', color: 'gray', border: 'solid', width: '100%', padding: 5, borderRadius: 5, marginTop: 5}}>
                            <StyledText variant="textTitle" style={{fontSize: 11, color: 'orange'}}>{sensor.type}</StyledText><StyledText variant="textTitle" style={{fontSize: 11, color: 'white'}}>    : {sensor.status}</StyledText>
                            <StyledText style={{fontSize: 6}}>{sensor.sensor_id}</StyledText>
                        </div>
                      )
                      }
                    )}
                    
                  </Grid>
                  <div style={{}}>
                    <StyledText style={{fontSize: 10, color: 'red', marginRight: 20, fontWeight: 'bold'}} variant="textTitle">Delete</StyledText>
                    <StyledText style={{fontSize: 10, color: 'black',fontWeight: 'bold'}} variant="textTitle">Edit</StyledText>
                  </div>
                </Grid>
              </Box>
            </Grid>
          );
        })}
      </Grid>
    </Grid>
  );
};

export default Dashboard;
