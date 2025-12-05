import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Button,
  Chip,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { getTaskDetails } from "@/api/allApi"; // your API call
import toast from "react-hot-toast";

export default function TaskDetail() {
  const { uuid } = useParams(); // get task uuid from URL
  const navigate = useNavigate();

  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch task details
  useEffect(() => {
    const fetchTaskDetails = async () => {
      try {
        setLoading(true);
        const res = await getTaskDetails(uuid);
        setTask(res || {});
      } catch (error) {
        console.error(error);
        toast.error("Failed to fetch task details");
      } finally {
        setLoading(false);
      }
    };
    fetchTaskDetails();
  }, [uuid]);

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 5 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!task) {
    return (
      <Box sx={{ textAlign: "center", mt: 5 }}>
        <Typography variant="h6">Task not found.</Typography>
        <Button variant="contained" sx={{ mt: 2 }} onClick={() => navigate(-1)}>
          Go Back
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3, maxWidth: 600, mx: "auto" }}>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate(-1)}
        sx={{ mb: 2 }}
      >
        Back
      </Button>

      <Card>
        <CardContent
          sx={{ display: "flex", flexDirection: "column", gap: 1.5 }}
        >
          <Typography variant="h6" sx={{ fontWeight: "bold" }}>
            Task Details
          </Typography>

          <Typography>
            <strong>User:</strong> {task.user || "-"}
          </Typography>
          <Typography>
            <strong>Category:</strong> {task.category || "-"}
          </Typography>
          <Typography>
            <strong>Task Name:</strong> {task.task_name || "-"}
          </Typography>
          <Typography>
            <strong>Hours:</strong> {task.hours || "-"}
          </Typography>
          <Typography>
            <strong>Status:</strong> {task.status || "-"}
            <Chip
              label={task.status || "-"}
              color={
                task.status === "Completed"
                  ? "success"
                  : task.status === "Pending"
                  ? "warning"
                  :task.status === "Blocked"
                  ? "error"
                  : "warning"
              }
              size="small"
            />
          </Typography>
          <Typography>
            <strong>Description:</strong> {task.description || "-"}
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
