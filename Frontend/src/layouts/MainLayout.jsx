import Topbar, { DrawerHeader, Main } from "@/components/Topbar";
import React from "react";
import { Outlet } from "react-router-dom";
import { MyAppContext } from "@/context/MyContext";
import { Box, CssBaseline } from "@mui/material";
import Sidebar from "@/components/Sidebar";

const MainLayout = () => {
  const { open, setOpen } = MyAppContext();

  return (
    <>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
      <Sidebar />

        <Main
          open={open}
          sx={{
            flexGrow: 1,
            bgcolor: "background.default",
            p: 3,
          }}
        >
            <Topbar />
          <DrawerHeader />

          <Outlet />
        </Main>
      </Box>
    </>
  );
};

export default MainLayout;
