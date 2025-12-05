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
  Autocomplete,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import { getCategoryName, getTaskList, getUserFilterName } from "@/api/allApi";
import Pagination from "@/components/Pagination";
import DateRange from "@/components/DateRange";

export default function TaskList() {
  const [selectedUser, setSelectedUser] = useState(""); // default all users
  const [selectedCategory, setSelectedCategory] = useState(""); // default all categories
  const [categories, setCategories] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [status, setStatus] = useState("");
  const [selectedDate, setSelectedDate] = useState(() => {
    const today = new Date();
    return today.toISOString().split("T")[0];
  });

  const tasksPerPage = 10;
  const navigate = useNavigate();

  // ---------------- FETCH USERS ----------------
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await getUserFilterName();
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
        // if (selectedUser === "") {
        //   for (const user of users) {
        //     const res = await getTaskList(
        //       user.uuid,
        //       selectedDate,
        //       selectedCategory || "",
        //       totalPages
        //     );
        //     const total = res.count
        //       ? Math.ceil(res.count / 10)
        //       : res.total_pages || 1;

        //     setTotalPages(total);

        //     allTasks = [...allTasks, ...(res?.results || [])];
        //   }

        //   setTasks(allTasks);
        //   return;
        // }

        // -----------------------------
        // CASE 2: SPECIFIC USER SELECTED
        // -----------------------------
        const response = await getTaskList(
          selectedUser,
          startDate,
          endDate,
          selectedCategory || "",
          currentPage,
          status
        );
        const total = response.count
          ? Math.ceil(response.count / 10)
          : res.total_pages || 1;

        setTotalPages(total);

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
  }, [selectedUser, startDate, endDate, selectedCategory, users, status]);

  // ---------------- VIEW TASK ----------------
  const handleView = (uuid) => {
    navigate(`${uuid}`);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  return (
    <Box sx={{ p: 3 }}>
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
      </Box>
      {/* Top Section */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          {/* CATEGORY FILTER */}
          <Autocomplete
            size="small"
            sx={{ minWidth: 180 }}
            options={[{ id: "", identity: "All Categories" }, ...categories]}
            getOptionLabel={(option) => option.identity}
            isOptionEqualToValue={(option, value) => option.id === value.id}
            clearOnEscape
            value={
              categories.find((c) => c.id === selectedCategory) || {
                id: "",
                identity: "All Categories",
              }
            }
            onChange={(e, newValue) => {
              setSelectedCategory(newValue?.id || "");
            }}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Category"
                InputLabelProps={{ shrink: true }}
              />
            )}
          />

          {/* DATE FILTER */}
          {/* <TextField
            label="Select Date"
            type="date"
            size="small"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            InputLabelProps={{ shrink: true }}
          /> */}

          <DateRange
            setStartDate={setStartDate}
            setEndDate={setEndDate}
            startedDate={startDate}
          />

          {/* STATUS FILTER */}
          <FormControl size="small" sx={{ width: "200px" }}>
            <InputLabel>Status</InputLabel>
            <Select
              label="Status"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              <MenuItem value="">All Status</MenuItem>
              <MenuItem value="Pending">Pending</MenuItem>
              <MenuItem value="Blocked">Blocked</MenuItem>
              {/* <MenuItem value="In_Progress">In Progress</MenuItem> */}
              <MenuItem value="Completed">Completed</MenuItem>
            </Select>
          </FormControl>

          {/* USER FILTER */}
          <Autocomplete
            size="small"
            sx={{ minWidth: 220 }}
            options={[
              { id: "", identity: "All Users", employee_id: "" },
              ...users,
            ]}
            getOptionLabel={(option) =>
              option.id === ""
                ? "All Users"
                : `${option.identity} (${option.employee_id})`
            }
            renderOption={(props, option) => (
              <li {...props}>
                {option.identity}
                {option.id !== "" && (
                  <span style={{ fontSize: "13px", marginLeft: 4 }}>
                    -({option.employee_id})
                  </span>
                )}
              </li>
            )}
            value={
              users.find((u) => u.id === selectedUser) || {
                id: "",
                identity: "All Users",
              }
            }
            onChange={(e, newValue) => {
              setSelectedUser(newValue?.id || "");
            }}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Select User"
                InputLabelProps={{ shrink: true }}
              />
            )}
          />
        </Box>
      </Box>

      {/* TASK TABLE */}
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="task table">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold" }}>S.No</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>User Name</TableCell>
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
                  <TableCell>
                    {" "}
                    {(currentPage - 1) * tasksPerPage + index + 1}
                  </TableCell>
                  <TableCell>{task.user_details?.identity || "-"}</TableCell>
                  <TableCell>
                    {task.category_details?.identity || "-"}
                  </TableCell>
                  <TableCell>{task.task_name || "-"}</TableCell>
                  <TableCell>
                    {task.created_at
                      ? new Date(task.created_at).toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                          hour12: true,
                        })
                      : "-"}
                  </TableCell>

                  <TableCell>
                    <Chip
                      label={task.status || "Pending"}
                      color={
                        task.status === "Completed"
                          ? "success"
                          : task.status === "In Progress"
                          ? "info"
                          : task.status === "Pending"
                          ? "warning"
                          : task.status === "Blocked"
                          ? "error"
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

      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
        maxVisiblePages={3}
      />
    </Box>
  );
}
