import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  Typography,
  Chip,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
} from "@mui/material";
import { getAttendanceDetails, getUserList, getUserName } from "@/api/allApi";

export default function AttendanceList() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedDate, setSelectedDate] = useState(() => {
    const today = new Date();
    return today.toISOString().split("T")[0]; // default today
  });

  // Fetch all users and auto-select the first one
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await getUserName();
        const userList = res?.results || [];
        setUsers(userList);

       setSelectedUser("");
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  //  Fetch attendance for selected user
  useEffect(() => {
    const fetchAttendance = async () => {
      try {
        setLoading(true);

        let allAttendance = [];

        // Case 1 — ALL USERS
        // if (selectedUser === "") {
        //   for (const user of users) {
        //     const res = await getAttendanceDetails(user.uuid, selectedDate);
        //     const list = res?.results || [];

        //     // Add username to each attendance entry
        //     const enriched = list.map((item) => ({
        //       ...item,
        //       userName: user.identity || user.email || "Unnamed User",
        //     }));

        //     allAttendance = [...allAttendance, ...enriched];
        //   }

        //   setAttendance(allAttendance);
        //   return;
        // }

        // Case 2 — SPECIFIC USER
        const response = await getAttendanceDetails(selectedUser, selectedDate);

        const enriched = (response?.results || []).map((item) => ({
          ...item,
          userName:
            users.find((u) => u.uuid === selectedUser)?.identity ||
            users.find((u) => u.uuid === selectedUser)?.email ||
            "Unnamed User",
        }));

        setAttendance(enriched);
      } catch (error) {
        console.error("Error fetching attendance:", error);
      } finally {
        setLoading(false);
      }
    };

    if (users.length > 0) fetchAttendance();
  }, [selectedUser, selectedDate, users]);

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Typography variant="h6" sx={{ fontWeight: "bold" }}>
          Attendance List
        </Typography>

        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          {/* Date Filter */}
          <TextField
            label="Select Date"
            type="date"
            size="small"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            InputLabelProps={{ shrink: true }}
          />
          {/* Dropdown to select user */}
          <FormControl size="small" sx={{ minWidth: 220 }}>
            <InputLabel shrink>Select User</InputLabel>
            <Select
              value={selectedUser}
              label="Select User"
              displayEmpty
              renderValue={(selected) => {
                if (selected === "") return "All Users";
                const user = users.find((u) => u.uuid === selected);
                return user?.identity || user?.email || "Unnamed User";
              }}
              onChange={(e) => setSelectedUser(e.target.value)}
            >
              <MenuItem value="">All Users</MenuItem>
              {users.map((user) => (
                <MenuItem key={user.uuid} value={user.uuid}>
                  {user.identity || user.email || "Unnamed User"}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </Box>

      {/*  Table */}
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 750 }} aria-label="attendance table">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold" }}>S.No</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Name</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Punch In</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Punch Out</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Punch Date</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Leave Status</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <CircularProgress size={28} />
                </TableCell>
              </TableRow>
            ) : attendance.length > 0 ? (
              attendance.map((item, index) => (
                <TableRow key={item.uuid}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>
                    {users.find((u) => u.uuid === selectedUser)?.identity ||
                      users.find((u) => u.uuid === selectedUser)?.email ||
                      "-"}
                  </TableCell>
                  <TableCell>{item.punch_in || "-"}</TableCell>
                  <TableCell>{item.punch_out || "-"}</TableCell>
                  <TableCell>{item.punch_date || "-"}</TableCell>
                  <TableCell>
                    <Chip
                      label={item.leave_status || "Unknown"}
                      color={
                        item.leave_status === "Present"
                          ? "success"
                          : item.leave_status === "Absent"
                          ? "error"
                          : "warning"
                      }
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  No attendance records found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
