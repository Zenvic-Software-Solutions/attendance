import {
  Divider,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  useTheme,
} from "@mui/material";
import React, { useContext } from "react";
import { DrawerHeader } from "./Topbar";
import APP_CONSTANTS from "@/config/AppConstants";
import { MyContext } from "@/context/MyContext";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import DashboardIcon from "@mui/icons-material/Dashboard";
import PeopleIcon from "@mui/icons-material/People";
import AssignmentIcon from "@mui/icons-material/Assignment";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import CategoryIcon from "@mui/icons-material/Category";
import CalenderTodayIcon from "@mui/icons-material/CalendarToday"
import { useNavigate } from "react-router-dom";

const Sidebar = () => {
  const { open, setOpen, setHovered, isTablet, currentDrawerWidth, hovered } =
    useContext(MyContext);
  const theme = useTheme();
  const navigate = useNavigate();

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const drawerItems = [
    { text: "Dashboard", icon: <DashboardIcon />, path: "/dashboard" },
    { text: "User", icon: <PeopleIcon />, path: "/user" },
    { text: "Task", icon: <AssignmentIcon />, path: "/task" },
    { text: "Attendance", icon: <AccessTimeIcon />, path: "/attendance" },
    { text: "Work Category", icon: <CategoryIcon />, path: "/work-category" },
    { text: "Leave", icon: <CalenderTodayIcon/>, path: "/leave" },
  ];
  return (
    <Drawer
      variant={isTablet ? "temporary" : "permanent"}
      open={open}
      onClose={() => setOpen(false)}
      onMouseEnter={() => !isTablet && setHovered(true)}
      onMouseLeave={() => !isTablet && setHovered(false)}
      sx={{
        width: isTablet ? 240 : currentDrawerWidth,
        flexShrink: 0,
        zIndex: isTablet ? 1300 : "auto",
        [`& .MuiDrawer-paper`]: {
          width: isTablet ? 240 : currentDrawerWidth,
          boxSizing: "border-box",
          transition: theme.transitions.create("width", {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
          }),
        },
      }}
      ModalProps={{
        BackdropProps: {
          sx: {
            backdropFilter: "blur(4px)",
            backgroundColor: "rgba(0,0,0,0.3)",
          },
        },
      }}
      disableScrollLock
    >
      <DrawerHeader
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: open ? "space-between" : "center", // icon only appears when open
          px: 2,
        }}
      >
        {/* Logo changes based on drawer state */}
        <img
          src={
            open || hovered
              ? APP_CONSTANTS.App_Logo
              : APP_CONSTANTS.App_Logo_Small
          }
          alt="Logo"
          style={{
            width: open || hovered ? "120px" : "40px", // adjust size if needed
            height: "auto",
            transition: "width 0.3s",
          }}
        />

        {/* Chevron icon only when drawer is open */}
        {open && (
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "ltr" ? (
              <ChevronLeftIcon />
            ) : (
              <ChevronRightIcon />
            )}
          </IconButton>
        )}
      </DrawerHeader>

      <Divider />

      <List>
        {drawerItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <ListItem key={item.text} disablePadding sx={{ display: "block" }}>
              <ListItemButton
                onClick={() => navigate(item.path)}
                sx={{
                  minHeight: 48,
                  justifyContent: open || hovered ? "initial" : "center",
                  px: 2.5,
                  backgroundColor: isActive ? "#f6f0f0ff" : "transparent",
                  borderRadius: "8px",
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open || hovered ? 3 : "auto",
                    justifyContent: "center",
                    color: isActive ? "#ab12f1ff" : "inherit",
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  sx={{
                    opacity: open || hovered ? 1 : 0,
                    color: isActive ? "#b626f9ff" : "inherit",
                  }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </Drawer>
  );
};

export default Sidebar;
