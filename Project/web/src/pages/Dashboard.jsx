import React,{useState, useEffect} from "react";
import { Box, Button, Grid, Input } from "@mui/material";
import Divider from "@mui/material/Divider";
import DeleteIcon from "@mui/icons-material/Delete";
import NewspaperSharpIcon from "@mui/icons-material/NewspaperSharp";
import { StyledText } from "../components/text/Text.styles";
import { useNavigate } from "react-router-dom";
import { catalogUrl, catalogPort, analyticUrl, analyticPort, commandUrl, commandPort } from "../generalConfig";
// import Image from "../components/avatar/Image";

const Dashboard = () => {

  const [houses, setHouses] = useState([]);
  const navigate = useNavigate();
  const [houseTitle, setHouseTitle] = useState('');
  const [houseAddress, setHouseAddress] = useState('');

  useEffect(() => {
    getHousesList();
  }, []);

  const getHousesList = () => {
    let userData = JSON.parse(localStorage.getItem("userData"));
    fetch(`${catalogUrl}${catalogPort}/house/allhouses?userId=${userData.user_id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${userData.password}`
      }
    }
    )
    .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        setHouses(data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const newHouse = () => {
    if (houseTitle === '' || houseAddress === '') {
      alert('Please fill in all fields');
      return;
    }
    let userData = JSON.parse(localStorage.getItem("userData"));
    fetch(`${catalogUrl}${catalogPort}/house/newhouse?userId=${userData.user_id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${userData.password}`
      },
      body: JSON.stringify({
        title: houseTitle,
        address: houseAddress
      })
    }
    )
    .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        getHousesList();
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const deleteHouse = (house_id) => {
    // let userData = JSON.parse(localStorage.getItem("userData"));
    // fetch(`${catalogUrl}${catalogPort}/house/deletehouse?userId=${userData.user_id}&houseId=${house_id}`, {
    //   method: 'DELETE',
    //   headers: {
    //     'Authorization': `Bearer ${userData.password}`
    //   }})
    // .then(response => response.json())
    //   .then(data => {
    //     console.log('Success:', data);
        
    //   })
    //   .catch((error) => {
    //     console.error('Error:', error);
    //   })
    //   .finally(() => {
    //     console.log('done');
    //     getHousesList();
    //   });
  }

  return (
    <Grid container sx={{ height: "", backgroundColor: "#353455" }}>
      <Grid container justifyContent="flex-start" style={{borderWidth: "10px", borderColor: 'green', borderBlock : 'solid', marginBottom: 10}}>
        <Button variant="contained" color="primary" onClick={()=>newHouse()} style={{margin: 10}}>Add House</Button>
        <Box sx={{ display: "flex", justifyContent: "flex-end", padding: 2 }}>
          <Input placeholder="House Title"  style={{marginRight: 10}} onChange={(e) => setHouseTitle(e.target.value)} />
          <Input placeholder="House Address" style={{marginRight: 10}} onChange={(e) => setHouseAddress(e.target.value)} />
        </Box>
      </Grid>
      <Grid container spacing={4} flex={1} height="100%">
        {houses && houses.map((item, index) => {
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
                      <Button onClick={()=>navigate('/sensor', {state: {house_id: item.house_id, house: item}})} style={{backgroundColor: 'green', color: 'white', borderRadius: 5, padding: 4, marginTop: 5, fontSize: 12}}>View Sensors</Button>
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
                    <Button variant="contained" color="primary" onClick={()=>deleteHouse(item.house_id)} style={{backgroundColor: 'darkred',fontSize: 8, marginTop: 3}}>Delete</Button>
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
