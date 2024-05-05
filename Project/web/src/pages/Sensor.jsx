import React,{useState, useEffect} from "react";
import { Box, Grid } from "@mui/material";
import Divider from "@mui/material/Divider";
import DeleteIcon from "@mui/icons-material/Delete";
import NewspaperSharpIcon from "@mui/icons-material/NewspaperSharp";
import { StyledText } from "../components/text/Text.styles";
import { useNavigate, useLocation} from "react-router-dom";
// import Image from "../components/avatar/Image";
import {catalogUrl, catalogPort, analyticUrl, analyticPort} from "../generalConfig";


const Dashboard = () => {

  const [sensors, setSensors] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const house_id = location.state.house_id;
  const houseData = location.state.house;
  const [sensorsData, setSensorsData] = useState([]);

  useEffect(() => {
    getSensorsList();
    viewSensorRecords();
  }, []);

  const getSensorsList = () => {
    let userData = JSON.parse(localStorage.getItem("userData"));
    userData.houses.map((item) => {
      if(item.house_id === house_id) {
        console.log(item.sensors);
        setSensors(item.sensors);
      }
    });
  }

  function findMinForSensorId(sensorId) {
    for (const item of sensorsData) {
      if (item.sensorId === sensorId) {
        console.log('item', item)
        return item
      }
    }
    return null; // Or handle the case where the sensor ID is not found
  }

  const viewSensorRecords = (sensor_ids) => {
    console.log('this is called !!!!')
    fetch(`${analyticUrl}${analyticPort}/analytic/fullAnalytics`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'access-control-allow-origin': '*',
      },
      body: JSON.stringify({
        sensorIds: ["3912fee4-af3f-43cf-9024-1c259f6a0459", "d04c5452-e9af-445b-adf4-415d7bfd31e7"],
        period: "4h"
    })
    }).then(response => response.json())
    .then(data => {
      console.log('RECORDS ___> ',data);
      setSensorsData(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });

  }

  return (
    <div>
      <StyledText variant="textTitle" style={{fontSize: 18, color: 'black'}}>{houseData.title}</StyledText>
      {sensors && sensors.map((item, index) => {
        if (item.type != 'AIR_CONDITIONER')
          return (
            <Grid key={index} item xs={12} md={6} lg={3}>
              <Box bgcolor="#0047b3" borderRadius={2} width="100%" height="150px" marginTop={2}>
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
                        {item.type} : {item.status}
                      </StyledText>
                        <StyledText style={{fontSize: 8}}>{item.sensor_id}</StyledText>
                        <Grid item>
                          <StyledText style={{fontSize: 12}}>Min: {findMinForSensorId(item.sensor_id)?  findMinForSensorId(item.sensor_id).min : 'N/A'}</StyledText>
                          <StyledText style={{fontSize: 12}}>Max: {findMinForSensorId(item.sensor_id)?  findMinForSensorId(item.sensor_id).max : 'N/A'}</StyledText>
                          <StyledText style={{fontSize: 12}}>Mean: {findMinForSensorId(item.sensor_id)?  findMinForSensorId(item.sensor_id).mean : 'N/A'}</StyledText>
                          <StyledText style={{fontSize: 12}}>Last Value: {findMinForSensorId(item.sensor_id)?  findMinForSensorId(item.sensor_id).lastValue : 'N/A'}</StyledText>
                        </Grid>

                    </Grid>
                  </Grid>
                </Grid>
              </Box>
            </Grid>
          )

        else
          return (
            <Grid key={index} item xs={12} md={6} lg={3}>
              <Box bgcolor="#0047b3" borderRadius={2} width="100%" height="200px" marginTop={2}>
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
                      {item.type} : {item.status}
                      </StyledText>
                        <StyledText style={{fontSize: 8}}>{item.sensor_id}</StyledText>

                        <Grid item>
                          <StyledText style={{fontSize: 12}}>Send a Manual Configuration for Air Conditioner</StyledText>
                          <input type="text" placeholder="Enter the temperature" style={{marginTop: 5, width: '80%'}}/>
                          <input type="text" placeholder="Enter the humidity" style={{marginTop: 5, width: '80%'}}/>
                          <input type="text" placeholder="Enter the status" style={{marginTop: 5, width: '80%'}}/>
                          <br/>
                          <button style={{backgroundColor: 'blue', color: 'white', borderRadius: 5, padding: 5, marginTop: 5}}>Send</button>
                        </Grid>

                    </Grid>
                  </Grid>
                </Grid>
              </Box>
            </Grid>
          )
}
    )}
    </div>
  );
};

export default Dashboard;
