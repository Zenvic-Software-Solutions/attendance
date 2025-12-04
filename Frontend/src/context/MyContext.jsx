import { useMediaQuery, useTheme } from "@mui/material";
import { createContext, useContext, useEffect, useState } from "react";

export const MyContext = createContext();

const MyProvider = ({ children }) => {
  const [open, setOpen] = useState(true);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const isTablet = useMediaQuery("(max-width:768px)");
  const [drawerWidth, setDrawerWidth] = useState(240);

  useEffect(() => {
    setDrawerWidth(open ? 240 : 86);
  }, [open]);
  useEffect(() => {
    if (isTablet) {
      setOpen(false); // Hide sidebar on tablet initially
    }
    setDrawerWidth(!isTablet ? 240 : 0);
  }, []);

  const [hovered, setHovered] = useState(false);
  // Determine dynamic width for hover
  const currentDrawerWidth = hovered ? 240 : drawerWidth;

  return (
    <MyContext.Provider
      value={{
        open,
        setOpen,
        drawerWidth,
        setDrawerWidth,
        isTablet,
        currentDrawerWidth,
        hovered,
        setHovered,
      }}
    >
      {children}
    </MyContext.Provider>
  );
};

export default MyProvider;

export const MyAppContext = () => useContext(MyContext);
