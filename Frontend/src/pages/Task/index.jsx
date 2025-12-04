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
  IconButton,
  Typography,
  Chip,
  CircularProgress,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import { getCategoryName, getTaskList, getUserName } from "@/api/allApi";

export default function TaskList() {
  const [selectedUser, setSelectedUser] = useState(""); // default all users
  const [selectedCategory, setSelectedCategory] = useState(""); // default all categories
  const [categories, setCategories] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  const [selectedDate, setSelectedDate] = useState(() => {
    const today = new Date();
    return today.toISOString().split("T")[0];
  });

  const navigate = useNavigate();

  // ---------------- FETCH USERS ----------------
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await getUserName();
        const userList = response?.results || [];
        setUsers(userList);
        setSelectedUser("");
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };
    fetchUsers();
  }, []);

  // ---------------- FETCH CATEGORIES ----------------
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await getCategoryName();
        const categoryList = response?.results || response || [];
        setCategories(categoryList);
        setSelectedCategory(""); // Always show "All Categories"
      } catch (error) {
        console.error("Error fetching categories:", error);
        toast.error("Error fetching categories");
      }
    };
    fetchCategories();
  }, []);

  // ---------------- FETCH TASKS ----------------

useEffect(() => {
  const fetchTasks = async () => {
    try {
      setLoading(true);

      let allTasks = [];

      // -----------------------------
      // CASE 1: "ALL USERS" SELECTED
      // -----------------------------
      if (selectedUser === "") {
        for (const user of users) {
          const res = await getTaskList(
            user.uuid,
            selectedDate,
            selectedCategory || ""
          );
          allTasks = [...allTasks, ...(res?.results || [])];
        }

        setTasks(allTasks);
        return;
      }

      // -----------------------------
      // CASE 2: SPECIFIC USER SELECTED
      // -----------------------------
      const response = await getTaskList(
        selectedUser,
        selectedDate,
        selectedCategory || ""
      );

      setTasks(response?.results || []);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    } finally {
      setLoading(false);
    }
  };

  // Only fetch after users list is loaded
  if (users.length > 0) {
    fetchTasks();
  }
}, [selectedUser, selectedDate, selectedCategory, users]);


  // ---------------- VIEW TASK ----------------
  const handleView = (uuid) => {
    navigate(`${uuid}`);
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Top Section */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Typography variant="h6" sx={{ fontWeight: "bold" }}>
          Task List
        </Typography>

        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          {/* CATEGORY FILTER */}
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel shrink>Category</InputLabel>
            <Select
              value={selectedCategory}
              label="Category"
              displayEmpty
              renderValue={(selected) =>
                selected === "" ? "All Categories" : selected
              }
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <MenuItem value="">All Categories</MenuItem>

              {categories.map((i) => (
                <MenuItem key={i.uuid} value={i.identity}>
                  {i.identity}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* DATE FILTER */}
          <TextField
            label="Select Date"
            type="date"
            size="small"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            InputLabelProps={{ shrink: true }}
          />

          {/* USER FILTER */}
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
                  {user.identity || user.email}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </Box>

      {/* TASK TABLE */}
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="task table">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold" }}>S.No</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Category</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Task Name</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Hours</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Status</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Action</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <CircularProgress size={28} />
                </TableCell>
              </TableRow>
            ) : tasks.length > 0 ? (
              tasks.map((task, index) => (
                <TableRow key={task.uuid}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{task.category || "-"}</TableCell>
                  <TableCell>{task.task_name || "-"}</TableCell>
                  <TableCell>{task.hours || "-"}</TableCell>
                  <TableCell>
                    <Chip
                      label={task.status || "Pending"}
                      color={
                        task.status === "Completed"
                          ? "success"
                          : task.status === "In Progress"
                          ? "warning"
                          : "default"
                      }
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <IconButton
                      color="primary"
                      onClick={() => handleView(task.uuid)}
                      aria-label="view task"
                    >
                      <VisibilityIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  No tasks found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
