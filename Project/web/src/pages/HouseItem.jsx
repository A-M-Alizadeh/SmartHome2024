import React,{useState, useEffect} from "react";
import { Box, Button, Grid, Input } from "@mui/material";
import Divider from "@mui/material/Divider";
import DeleteIcon from "@mui/icons-material/Delete";
import NewspaperSharpIcon from "@mui/icons-material/NewspaperSharp";
import { StyledText } from "../components/text/Text.styles";
import { useNavigate } from "react-router-dom";
// import Image from "../components/avatar/Image";

const HouseItem = ({house, deleteHouse, editHouse}) => {
    const navigate = useNavigate();
    const [editMode, setEditMode] = useState(false);
    const [title, setTitle] = useState(house.title);
    const [address, setAddress] = useState(house.address);

    const handleEditButton = () => {
      if (editMode) {
        editHouse(house.house_id, title, address);
      }
      setEditMode(!editMode);
    };

    return (
        <Grid item xs={12} md={6} lg={3}>
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
                {editMode ? (
                  <div>
                    <Input placeholder="House Title"  style={{marginRight: 10, color: 'white'}} onChange={(e) => setTitle(e.target.value)} value={title} />
                    <Input placeholder="House Address" style={{marginRight: 10, color: 'white'}} onChange={(e) => setAddress(e.target.value)} value={address} />
                  </div>
                ) : (
                  <Grid item>
                    <StyledText variant="textTitle" style={{fontSize: 18}}>
                      {house.title}
                    </StyledText>
                    <Grid
                      item
                    >
                      <StyledText style={{fontSize: 12}}>{house.address}</StyledText>
                    </Grid>
                    <StyledText style={{fontSize: 8}}>{house.house_id}</StyledText>
                  </Grid>
                )}
              </Grid>
                  <Button onClick={()=>navigate('/sensor', {state: {house_id: house.house_id, house: house}})} style={{backgroundColor: 'green', color: 'white', borderRadius: 5, padding: 4, marginTop: 5, fontSize: 12}}>View Sensors</Button>
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
                {house.sensors.map((sensor, index) => {
                  return (
                    <div key={index} style={{ borderWidth: '1px', color: 'gray', border: 'solid', width: '100%', padding: 5, borderRadius: 5, marginTop: 5}}>
                        <StyledText variant="textTitle" style={{fontSize: 11, color: 'orange'}}>{sensor.type}</StyledText><StyledText variant="textTitle" style={{fontSize: 11, color: 'white'}}>    : {sensor.status}</StyledText>
                        <StyledText style={{fontSize: 6}}>{sensor.sensor_id}</StyledText>
                    </div>
                  )
                  }
                )}
                
              </Grid>
              <div style={{justifyContent: 'space-between'}}>
                <Button variant="contained" color="primary" onClick={()=>deleteHouse(house.house_id)} style={{backgroundColor: 'darkred',fontSize: 8, marginTop: 3, marginRight: 122}}>Delete</Button>
                <Button variant="contained" color="primary" onClick={()=>handleEditButton()} style={{backgroundColor: editMode? 'green' : 'orange',fontSize: 8, marginTop: 3}}>{editMode ? "Save" : "Edit"}</Button>
              </div>
            </Grid>
          </Box>
        </Grid>
      );
  };

export default HouseItem;
