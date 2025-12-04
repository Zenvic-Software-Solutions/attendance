import React, { useContext, useState } from "react";
import { styled, useTheme } from "@mui/material/styles";
import {
    Drawer,
    Toolbar,
    List,
    Typography,
    Divider,
    IconButton,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    AppBar as MuiAppBar,
    Box,
    Button,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import DashboardIcon from "@mui/icons-material/Dashboard";
import PeopleIcon from "@mui/icons-material/People";
import AssignmentIcon from "@mui/icons-material/Assignment";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import CategoryIcon from "@mui/icons-material/Category";
import LogoutIcon from "@mui/icons-material/Logout";
import { MyContext } from "@/context/MyContext";
import { useNavigate, useLocation } from "react-router-dom";
import LogoutModal from "./LogoutModal";
import toast from "react-hot-toast";
import APP_CONSTANTS from "@/config/AppConstants";
import ExitToAppIcon from '@mui/icons-material/ExitToApp';

const drawerWidth = 240;
const closedDrawerWidth = 60;



export const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
    ({ theme, open }) => ({
        flexGrow: 1,
        padding: theme.spacing(3),
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    })
);


const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
    transition: theme.transitions.create(['margin', 'width'], {
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


export const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(0, 1),

    ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
}));

const drawerItems = [
    { text: "Dashboard", icon: <DashboardIcon />, path: "/dashboard" },
    { text: "User", icon: <PeopleIcon />, path: "/user" },
    { text: "Task", icon: <AssignmentIcon />, path: "/task" },
    { text: "Attendance", icon: <AccessTimeIcon />, path: "/attendance" },
    { text: "Work Category", icon: <CategoryIcon />, path: "/work-category" },
    {text: "Leave",icon: <ExitToAppIcon/>, path:"/exittoapp"}
];




export default function Topbar() {
    const theme = useTheme();
    const navigate = useNavigate();
    const { open, setOpen } = useContext(MyContext);
    const [logoutDialog, setLogoutDialog] = useState(false);

    const location = useLocation();

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

            <AppBar position="fixed" open={open}>
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
                                <MenuIcon />
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



            <Drawer
                variant="permanent"
                anchor='left'
                open={true}
                sx={{
                    width: open ? drawerWidth : closedDrawerWidth,
                    flexShrink: 0,
                    "& .MuiDrawer-paper": {
                        width: open ? drawerWidth : closedDrawerWidth,
                        transition: theme.transitions.create("width", {
                            easing: theme.transitions.easing.sharp,
                            duration: theme.transitions.duration.enteringScreen,
                        }),
                        overflowX: "hidden",
                        boxSizing: "border-box",
                    },
                }}
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
                        src={open ? APP_CONSTANTS.App_Logo : APP_CONSTANTS.App_Logo_Small}
                        alt="Logo"
                        style={{
                            width: open ? "120px" : "40px", // adjust size if needed
                            height: "auto",
                            transition: "width 0.3s",
                        }}
                    />

                    {/* Chevron icon only when drawer is open */}
                    {open && (
                        <IconButton onClick={handleDrawerClose}>
                            {theme.direction === "ltr" ? <ChevronLeftIcon /> : <ChevronRightIcon />}
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
                                        justifyContent: open ? "initial" : "center",
                                        px: 2.5,
                                        backgroundColor: isActive ? "#f6f0f0ff" : "transparent",
                                        borderRadius: "8px",
                                    }}
                                >
                                    <ListItemIcon
                                        sx={{
                                            minWidth: 0,
                                            mr: open ? 3 : "auto",
                                            justifyContent: "center",
                                            color: isActive ? "#ab12f1ff" : "inherit",
                                        }}
                                    >
                                        {item.icon}
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={item.text}
                                        sx={{
                                            opacity: open ? 1 : 0,
                                            color: isActive ? "#b626f9ff" : "inherit",
                                        }}
                                    />
                                </ListItemButton>
                            </ListItem>
                        );
                    })}
                </List>


            </Drawer>

            {/* Logout Confirmation Modal */}
            <LogoutModal
                open={logoutDialog}
                onCancel={cancelLogout}
                onConfirm={confirmLogout}
            />

        </>
    );
}
