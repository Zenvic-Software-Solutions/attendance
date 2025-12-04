import Topbar, { DrawerHeader, Main } from '@/components/Topbar'
import React from 'react'
import { Outlet } from 'react-router-dom'
import { MyAppContext } from '@/context/MyContext';
import { Box, CssBaseline } from '@mui/material';


const MainLayout = () => {
  const { open, setOpen } = MyAppContext();

  return (
    <>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <Topbar />

        <Main open={open}>
          <DrawerHeader />
        
          <Outlet />
        </Main>
      </Box>

    </>
  )
}

export default MainLayout