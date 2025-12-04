import React, { useEffect, useState } from "react"; import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Avatar,
  CircularProgress,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CancelIcon from "@mui/icons-material/Cancel";
import GroupIcon from "@mui/icons-material/Group";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import EventBusyIcon from "@mui/icons-material/EventBusy";
import { getAttendanceDashboard } from "@/api/allApi"; 

const AttendanceDashboard = () => {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch data on component mount
  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const res = await getAttendanceDashboard();

      if (res) {
        setData(res);
      } else {
        toast.error("Failed to load dashboard data");
      }
    } catch (error) {
      console.error("Dashboard fetch error:", error);
      toast.error("Something went wrong fetching data");
    } finally {
      setLoading(false);
    }
  };

  // Dynamic stats (mapped from API)
  const stats = [
    {
      title: "Present Today",
      value: data?.present_count ?? "-",
      icon: <CheckCircleIcon sx={{ fontSize: 30, color: "white" }} />,
      iconBg: "#34a853",
    },
    {
      title: "Absent Today",
      value: data?.absent_count ?? "-",
      icon: <CancelIcon sx={{ fontSize: 30, color: "white" }} />,
      iconBg: "#f44336",
    },
    {
      title: "Total Employees",
      value: data?.employee_count ?? "-",
      icon: <GroupIcon sx={{ fontSize: 30, color: "white" }} />,
      iconBg: "#03a9f4",
    },
    {
      title: "Monthly Present",
      value: data?.month_present_count ?? "-",
      icon: <EventAvailableIcon sx={{ fontSize: 30, color: "white" }} />,
      iconBg: "#ff9800",
    },
    {
      title: "Monthly Absent",
      value: data?.month_absent_count ?? "-",
      icon: <EventBusyIcon sx={{ fontSize: 30, color: "white" }} />,
      iconBg: "#9c27b0",
    },
  ];



  return (
    <Box sx={{ p: 3, minHeight: "100vh" }}>
      {loading ? (
        <Box sx={{ textAlign: "center", mt: 10 }}>
          <CircularProgress />
          <Typography sx={{ mt: 2 }}>Loading Dashboard...</Typography>
        </Box>
      ) : (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {stats.map((stat, index) => (
            <Grid size={{ xs: 12, md: 3 }} key={index}>
              <Card
                sx={{
                  borderRadius: "12px",
                  boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
                  background:
                    "linear-gradient(to bottom right, #f8fbff, #eef3fa)",
                  transition: "all 0.3s ease",
                  "&:hover": { boxShadow: "0 6px 16px rgba(0,0,0,0.15)" },
                  height: "100%",
                  minHeight: "120px",
                }}
              >
                <CardContent
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    p: "20px !important",
                    height: "100%",
                  }}
                >
                  <Box sx={{ flex: 1 }}>
                    <Typography
                      variant="subtitle2"
                      sx={{
                        fontWeight: 600,
                        color: "#6c757d",
                        mb: 0.5,
                        fontSize: "0.875rem",
                      }}
                    >
                      {stat.title}
                    </Typography>
                    <Typography
                      variant="h5"
                      sx={{
                        fontWeight: 700,
                        color: "#000",
                        fontSize: "1.75rem",
                      }}
                    >
                      {stat.value}
                    </Typography>
                  </Box>
                  <Avatar
                    sx={{
                      bgcolor: stat.iconBg,
                      width: 64,
                      height: 64,
                      boxShadow: "0 4px 10px rgba(0,0,0,0.15)",
                      ml: 2,
                    }}
                  >
                    {stat.icon}
                  </Avatar>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default AttendanceDashboard;
