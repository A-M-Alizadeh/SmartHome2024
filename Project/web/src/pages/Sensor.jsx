import React, { useState, useEffect } from "react";
import { Box, Button, FormControl, Grid, Input, InputLabel, MenuItem, Select } from "@mui/material";
import Divider from "@mui/material/Divider";
import DeleteIcon from "@mui/icons-material/Delete";
import NewspaperSharpIcon from "@mui/icons-material/NewspaperSharp";
import { StyledText } from "../components/text/Text.styles";
import { useNavigate, useLocation } from "react-router-dom";
// import Image from "../components/avatar/Image";
import { catalogUrl, catalogPort, analyticUrl, analyticPort, commandUrl, commandPort } from "../generalConfig";
import SelectInput from "@mui/material/Select/SelectInput";
import { LineChart } from '@mui/x-charts/LineChart';


const Dashboard = () => {

  const [sensors, setSensors] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const house_id = location.state.house_id;
  const houseData = location.state.house;
  const [sensorsData, setSensorsData] = useState([]);
  const [commandStatus, setCommandStatus] = useState(null);
  const [tempValue, setTempValue] = useState(null);
  const [humidValue, setHumidValue] = useState(null);
  const [statusValue, setStatusValue] = useState("ON");
  const [newSensorType, setNewSensorType] = useState("TEMPERATURE");
  const [tempChartData, setTempChartData] = useState(null);
  const [humidChartData, setHumidChartData] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState("5m");


  useEffect(() => {
    getSensorsList();
  }, []);

  const getSensorsList = () => {
    let userData = JSON.parse(localStorage.getItem("userData"));
    fetch(`${catalogUrl}${catalogPort}/device/allsensors?userId=${userData.user_id}&houseId=${house_id}`, {
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
        setSensors(data);
        viewSensorRecords(findTemp_Humid_SensorIds(data));
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const findTemp_Humid_SensorIds = (sensors) => {
    let temp_humid_sensors = [];
    sensors.map((item) => {
      if (item.type === 'TEMPERATURE' || item.type === 'HUMIDITY') {
        temp_humid_sensors.push(item.sensor_id);
      }
    });
    return temp_humid_sensors;
  }

  function findMinForSensorId(sensorId) {
    for (const item of sensorsData) {
      if (item.sensorId === sensorId) {
        // console.log('item', item)
        return item
      }
    }
    return null; // Or handle the case where the sensor ID is not found
  }

  const newSensor = () => {
    if (newSensorType === '') {
      alert('Please fill in all fields');
      return;
    }
    let userData = JSON.parse(localStorage.getItem("userData"));
    fetch(`${catalogUrl}${catalogPort}/device/newsensor?userId=${userData.user_id}&houseId=${house_id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${userData.password}`
      },
      body: JSON.stringify({
        type: newSensorType
      })
    }).then(response => response.json())
      .then(data => {
        // console.log('Success:', data);
        getSensorsList();
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const viewSensorRecords = (sensor_ids, period) => {
    setSelectedPeriod(period);
    // console.log('SENSOR IDS', sensor_ids);
    fetch(`${analyticUrl}${analyticPort}/analytic/fullAnalytics`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'access-control-allow-origin': '*',
      },
      body: JSON.stringify({
        sensorIds: sensor_ids,
        period: period
      })
    }).then(response => response.json())
      .then(data => {
        console.log('RECORDS ___> ', data);
        setSensorsData(data);
        handleChartsData(data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const handleChartsData = (data) => {
    let tempData_date = [];
    let tempData_value = [];
    let humidData_date = [];
    let humidData_value = [];

    data.map((item) => {
      if (item.type === 'temperature') {
        // tempData_date = item.records.map((record) => record.date);
        tempData_value = item.records.map((record) => record.value);
      }
      else if (item.type === 'humidity') {
        // humidData_date = item.records.map((record) => record.date);
        humidData_value = item.records.map((record) => record.value);
      }
    });
    setTempChartData({ date: tempData_date, value: tempData_value });
    setHumidChartData({ date: humidData_date, value: humidData_value });
  }


  const sendCommand = (airSensorId) => {

    if (!tempValue || !humidValue || !statusValue) {
      alert('Please fill all the fields');
      return;
    }
    
    let userId = JSON.parse(localStorage.getItem("userData"))["user_id"];
    console.log('BODY', JSON.stringify({
      userId: userId,
      houseId: house_id,
      sensorId: airSensorId,
      temperature: parseFloat(tempValue),
      humidity: parseFloat(humidValue),
      status: statusValue,
      actionType: "manual"
    }))
    fetch(`${commandUrl}${commandPort}/command/airConiditioner`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'access-control-allow-origin': '*',
      },
      body: JSON.stringify({
        userId: userId,
        houseId: house_id,
        sensorId: airSensorId,
        temperature: parseFloat(tempValue),
        humidity: parseFloat(humidValue),
        status: statusValue,
        actionType: "manual"
      })
    }).then(response => response.json())
      .then(data => {
        // console.log('Command ___> ', data);
        setCommandStatus(data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const deleteSensor = (sensor_id) => {
    let userData = JSON.parse(localStorage.getItem("userData"));
    fetch(`${catalogUrl}${catalogPort}/device/deletesensor?userId=${userData.user_id}&houseId=${house_id}&sensorId=${sensor_id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${userData.password}`
      }
    }).then(response => response.json())
      .then(data => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      })
      .finally(() => {
        getSensorsList();
      });
  }

  return (
    <div>
      <StyledText variant="textTitle" style={{ fontSize: 18, color: 'black' }}>{houseData.title}</StyledText>
      <Grid container justifyContent="flex-start" style={{borderWidth: "10px", borderColor: 'green', borderBlock : 'solid', marginBottom: 10}}>
        <Button variant="contained" color="primary" style={{margin: 10}} onClick={()=>newSensor()}>Add Sensor</Button>
        <Box sx={{ display: "flex", justifyContent: "flex-end", padding: 0 }}>
          <Select 
            style={{ width: '100%', backgroundColor: 'white', borderRadius: 8, fontSize: 14}} 
            value={newSensorType}
            onChange={(e) => setNewSensorType(e.target.value)}
            >
              <MenuItem value="TEMPERATURE">TEMPERATURE</MenuItem>
              <MenuItem value="HUMIDITY">HUMIDITY</MenuItem>
              <MenuItem value="AIR_CONDITIONER">AIR_CONDITIONER</MenuItem>
          </Select>
        </Box>
      </Grid>
          <FormControl fullWidth>
            <InputLabel id="demo-simple-select-label">Period</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={selectedPeriod}
              label="Period"
              onChange={(e) => viewSensorRecords(findTemp_Humid_SensorIds(sensors), e.target.value)}
            >
              <MenuItem value="1m">1 Minute</MenuItem>
              <MenuItem value="5m">5 Minutes</MenuItem>
              <MenuItem value="15m">15 Minutes</MenuItem>
              <MenuItem value="2h">2 Hours</MenuItem>
              <MenuItem value="4h">4 Hours</MenuItem>
              <MenuItem value="1d">1 Day</MenuItem>
              <MenuItem value="7d">7 Days</MenuItem>
            </Select>
          </FormControl>
      <Box sx={{ display: "flex", justifyContent: "flex-start", padding: 0 }}>
        <LineChart
          series={[
            { curve: "linear", data: humidChartData ? humidChartData.value : [1, 2, 3, 4, 5, 6] , label: "Humidity", color: '#4e79a7'},
          ]}
          width={1000}
          height={400}
        />
        <LineChart
          series={[
            { curve: "linear", data: tempChartData ? tempChartData.value : [1, 2, 3, 4, 5, 6], label: "Temperature", color: '#e15759' }
          ]}
          width={1000}
          height={400}
        />
      </Box>
      {sensors && sensors.map((item, index) => {
        if (item.type != 'AIR_CONDITIONER')
          return (
            <Grid key={index} item xs={12} md={6} lg={3}>
              <Box bgcolor="#0047b3" borderRadius={2} width="100%" height="180px" marginTop={2}>
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
                      <StyledText variant="textTitle" style={{ fontSize: 18 }}>
                        {item.type} : {item.status}
                      </StyledText>
                      <StyledText style={{ fontSize: 8 }}>{item.sensor_id}</StyledText>
                      <Grid item>
                        <StyledText style={{ fontSize: 12 }}>Min: {findMinForSensorId(item.sensor_id) ? findMinForSensorId(item.sensor_id).min : 'N/A'}</StyledText>
                        <StyledText style={{ fontSize: 12 }}>Max: {findMinForSensorId(item.sensor_id) ? findMinForSensorId(item.sensor_id).max : 'N/A'}</StyledText>
                        <StyledText style={{ fontSize: 12 }}>Mean: {findMinForSensorId(item.sensor_id) ? findMinForSensorId(item.sensor_id).mean : 'N/A'}</StyledText>
                        <StyledText style={{ fontSize: 12 }}>Last Value: {findMinForSensorId(item.sensor_id) ? findMinForSensorId(item.sensor_id).lastValue : 'N/A'}</StyledText>
                      </Grid>
                      <Button 
                        onClick={()=> deleteSensor(item.sensor_id)}
                        style={{backgroundColor: 'orange', color: 'white', borderRadius: 5, padding: 4, marginTop: 5, fontSize: 12}}>
                        Delete
                      </Button>

                    </Grid>
                  </Grid>
                </Grid>
              </Box>
            </Grid>
          )

        else
          return (
            <Grid key={index} item xs={12} md={6} lg={3}>
              <Box bgcolor="#0047b3" borderRadius={2} width="100%" height="250px" marginTop={2}>
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
                      <StyledText variant="textTitle" style={{ fontSize: 18 }}>
                        {item.type} : {commandStatus ? commandStatus.data.status : item.status}
                      </StyledText>
                      <StyledText style={{ fontSize: 8 }}>{item.sensor_id}</StyledText>

                      <Grid item>
                        <StyledText style={{ fontSize: 12 }}>Send a Manual Configuration for Air Conditioner</StyledText>
                        <Input
                          type="text"
                          placeholder="Enter the temperature"
                          onChange={(e) => setTempValue(e.target.value)}
                          value={tempValue}
                          style={{ marginTop: 5, width: '80%', backgroundColor: 'white', borderRadius: 8 }} />
                        <Input 
                        type="text" 
                        placeholder="Enter the humidity"
                        onChange={(e) => setHumidValue(e.target.value)}
                        value={humidValue}
                        style={{ marginTop: 5, width: '80%', backgroundColor: 'white', borderRadius: 8 }} />
                        <Select 
                        style={{ marginTop: 5, width: '80%', backgroundColor: 'white', borderRadius: 8 }} 
                        value={statusValue}
                        onChange={(e) => setStatusValue(e.target.value)}
                        >
                          <MenuItem value="ON">ON</MenuItem>
                          <MenuItem value="OFF">OFF</MenuItem>
                        </Select>
                        <br />
                        <Button style={{ backgroundColor: 'green', color: 'white', borderRadius: 5, padding: 5, marginTop: 5 }} onClick={() => sendCommand(item.sensor_id)}>Send</Button>
                        {commandStatus ? commandStatus.status : ''}
                        <Button 
                        onClick={()=> deleteSensor(item.sensor_id)}
                        style={{backgroundColor: 'orange', color: 'white', borderRadius: 5, padding: 5, marginLeft: 10, marginTop: 5, fontSize: 12}}>
                          Delete
                        </Button>
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
