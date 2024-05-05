import React,{useState, useEffect} from "react";
import { Box, Grid } from "@mui/material";
import Divider from "@mui/material/Divider";
import DeleteIcon from "@mui/icons-material/Delete";
import NewspaperSharpIcon from "@mui/icons-material/NewspaperSharp";
import { StyledText } from "../components/text/Text.styles";
import { useNavigate, useLocation} from "react-router-dom";
// import Image from "../components/avatar/Image";
import {catalogUrl, catalogPort, analyticUrl, analyticPort, commandUrl, commandPort} from "../generalConfig";


const Dashboard = () => {

  const [sensors, setSensors] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const house_id = location.state.house_id;
  const houseData = location.state.house;
  const [sensorsData, setSensorsData] = useState([]);
  const [commandStatus, setCommandStatus] = useState(null);

  useEffect(() => {
    getSensorsList();
  }, []);

  const getSensorsList = () => {
    let userData = JSON.parse(localStorage.getItem("userData"));
    userData.houses.map((item) => {
      if(item.house_id === house_id) {
        // console.log(item.sensors);
        setSensors(item.sensors);
        viewSensorRecords(findTemp_Humid_SensorIds(item.sensors));
      }
    });
  }

  const findTemp_Humid_SensorIds = (sensors) => {
    let temp_humid_sensors = [];
    sensors.map((item) => {
      if(item.type === 'TEMPERATURE' || item.type === 'HUMIDITY') {
        temp_humid_sensors.push(item.sensor_id);
      }
    });
    return temp_humid_sensors;
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
    console.log('SENSOR IDS', sensor_ids);
    fetch(`${analyticUrl}${analyticPort}/analytic/fullAnalytics`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'access-control-allow-origin': '*',
      },
      body: JSON.stringify({
        sensorIds: sensor_ids,
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

  const sendCommand = () => {
    fetch(`${commandUrl}${commandPort}/command/airConiditioner`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'access-control-allow-origin': '*',
      },
      body: JSON.stringify({
          sensorId: "e8073adc-38a8-44e6-a8e2-532bce5cd8bb",
          temperature: 50,
          humidity: 20,
          status: "ON",
          actionType: "manual"
      })
    }).then(response => response.json())
    .then(data => {
      setCommandStatus(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

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
                      {item.type} : {commandStatus? commandStatus.data.status : item.status}
                      </StyledText>
                        <StyledText style={{fontSize: 8}}>{item.sensor_id}</StyledText>

                        <Grid item>
                          <StyledText style={{fontSize: 12}}>Send a Manual Configuration for Air Conditioner</StyledText>
                          <input type="text" placeholder="Enter the temperature" style={{marginTop: 5, width: '80%'}}/>
                          <input type="text" placeholder="Enter the humidity" style={{marginTop: 5, width: '80%'}}/>
                          <input type="text" placeholder="Enter the status" style={{marginTop: 5, width: '80%'}}/>
                          <br/>
                          <button style={{backgroundColor: 'blue', color: 'white', borderRadius: 5, padding: 5, marginTop: 5}} onClick={()=>sendCommand()}>Send</button>
                          {commandStatus? commandStatus.status : ''}
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
