import React, { useContext, useState } from "react";
import { styled } from "@mui/material/styles";
import {
  Toolbar,
  Typography,
  IconButton,
  AppBar as MuiAppBar,
  Box,
  Button,
  useMediaQuery,
} from "@mui/material";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import LogoutIcon from "@mui/icons-material/Logout";
import { MyContext } from "@/context/MyContext";
import { useNavigate, useLocation } from "react-router-dom";
import LogoutModal from "./LogoutModal";
import toast from "react-hot-toast";


const drawerWidth = 240;
const closedDrawerWidth = 60;

export const Main = styled("main", {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  transition: theme.transitions.create("margin", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
}));

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  transition: theme.transitions.create(["margin", "width"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
    // zIndex: theme.zIndex.drawer + 1,
  }),
  backgroundColor: "#fff",
  color: "#000",
  ...(open
    ? {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: `${drawerWidth}px`,
      }
    : {
        width: `calc(100% - ${closedDrawerWidth}px)`,
        marginLeft: `${closedDrawerWidth}px`,
      }),
}));

export const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),

  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));



export default function Topbar() {
  const navigate = useNavigate();

  const { open, setOpen, setHovered, isTablet, currentDrawerWidth, hovered } =
    useContext(MyContext);
  const [logoutDialog, setLogoutDialog] = useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleLogout = () => {
    setLogoutDialog(true);
  };

  const confirmLogout = () => {
    localStorage.removeItem("token");
    toast.success("Successfully logged out!");
    setLogoutDialog(false);
    setTimeout(() => {
      navigate("/");
    }, 500);
  };

  const cancelLogout = () => {
    setLogoutDialog(false);
  };

  return (
    <>
      <AppBar
        position="fixed"
        sx={{
          width: isTablet ? "100%" : `calc(100% - ${currentDrawerWidth}px)`,
          ml: isTablet || hovered ? 0 : `${currentDrawerWidth}px`,
          transition: "all 0.3s ease",
        }}
      >
        <Toolbar
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            px: 2,
          }}
        >
          {/* Left side: Menu Icon & Title */}
          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            {!open && (
              <IconButton
                color="inherit"
                onClick={() => setOpen(true)}
                sx={{
                  color: "black",
                }}
              >
                <ArrowForwardIcon />
              </IconButton>
            )}

            <Typography
              variant="h6"
              component="div"
              sx={{
                fontWeight: 700,
                color: "#222",
                fontSize: "1.25rem",
                letterSpacing: "0.5px",
                fontFamily: "'Poppins', sans-serif",
              }}
            >
              Zenvic Attendance
            </Typography>
          </Box>

          {/* Right side: Logout */}
          <Box>
            <Button
              variant="contained"
              color="error"
              startIcon={<LogoutIcon />}
              onClick={handleLogout}
              sx={{
                textTransform: "none",
                fontWeight: 600,
                borderRadius: "8px",
              }}
            >
              Logout
            </Button>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Logout Confirmation Modal */}
      <LogoutModal
        open={logoutDialog}
        onCancel={cancelLogout}
        onConfirm={confirmLogout}
      />
    </>
  );
}
