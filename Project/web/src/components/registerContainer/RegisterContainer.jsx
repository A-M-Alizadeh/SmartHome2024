import { Grid } from '@mui/material'
import React from 'react'

const RegisterContainer = ({children,sx,backgroundColor}) => {
  return (
    <Grid
    item
    container
    alignContent={"flex-start"}
    justifyContent={"center"}
    border={'1px solid rgba(255,255,255,0.5)'}
    // backgroundColor={backgroundColor}
    boxShadow={'1px 2px 10px 0px rgba(255, 255, 255, 0.5)'}
    borderRadius={3}
    // sx={{ width: {xs:320, sm:350, md: 380 }, height: {xs:360,sm:390, md: 430 } }}
    sx={sx}
  >
    {children}
  </Grid>
  )
}

export default RegisterContainer;