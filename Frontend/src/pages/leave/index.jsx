import React, { useEffect, useState, } from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  TextField,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel,
  Chip,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogContent,
  DialogActions,
  DialogTitle,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Paper,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { getUserLeaveList } from "@/api/allApi";
// import { v4 as uuid } from "uuid";


const UserLeaveList = () => {
  const [leaveData, setLeaveData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modal States
  const [statusModalOpen, setStatusModalOpen] = useState(false);
  const [selectedUserForStatus, setSelectedUserForStatus] = useState(null);
  const[filterName,setFilterName]=useState("")
    const [search, setSearch] = useState("");
    const [users, setUsers] = useState([]);
    const[userList,setUserList]=useState([]);

    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const usersPerPage = 10;
    const navigate = useNavigate();
      useEffect(() => {
        const fetchUsers = async () => {
          try {
            const response = await getUserLeaveList();
            const userList = response?.results || [];
            setUsers(userList);
            setSelectedUser("");
          } catch (error) {
            console.error("Error fetching users:", error);
          }
        };
        fetchUsers();
      }, []);
  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      fetchUsers();
    }, 400);
    return () => clearTimeout(delayDebounce);
  }, [currentPage, search]);

  useEffect(() => {
    setCurrentPage(1);
  }, [search]);

  const fetchUsers = async () => {
    try {
      const response = await getUserLeaveList(currentPage, search);
      if (response) {
          const id = uuid(); // now works
        setUsers(response?.results || []);

        const total = response.count
          ? Math.ceil(response.count / 10)
          : response.total_pages || 1;

        setTotalPages(total);
      } else {
        toast.error("No user data found!");
        setUsers([]);
        setTotalPages(1);
      }
    } catch (error) {
      console.log("Error fetching users:", error);
      toast.error("Error fetching users");
    }
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleView = (uuid) => {
    navigate(`${uuid}`);
  };
  const defaultLeaveData = [
  {
    id: 1,
    username: "Hari Haran",
    leaveType: "Sick Leave",
    startDate: "2025-12-01",
    endDate: "2025-12-03",
    totalDays: 3,
    status: "Rejected",
  },
  {
    id: 2,
    username: "Arun Kumar",
    leaveType: "Casual Leave",
    startDate: "2025-12-10",
    endDate: "2025-12-11",
    totalDays: 2,
    status: "Approved",
  },
];

  
  return (
    <Box sx={{ p: 3, }}>
        <Box sx={{display:"flex",justifyContent:"space-between",alignItems: "center",
          mb: 2,}}>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: "bold" }}>
        Leave Requests
    
      </Typography>
        <TextField 
          label="Select username"
          
          variant="outlined"
          size="small"
          sx={{mb:2 ,width: "250px",gap:2}}
          value={filterName}
          onChange={(e) => setFilterName(e.target.value)}
          
        />
  <FormControl sx={{ mb: 2,width:"200px",justifyContent:"center", gap:2 }}>
    
        <InputLabel>Status</InputLabel>
        <Select size="small" 
          label="Status"
           variant="outlined"
           sx={{alignItems: "center",justifyContent:""}}
         
         
        >
          <MenuItem value="">All</MenuItem>
          <MenuItem value="Approved">Approved</MenuItem>
          <MenuItem value="Pending">Pending</MenuItem>
          <MenuItem value="Rejected">Rejected</MenuItem>
        </Select>
       
      </FormControl>
        </Box>
      <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
             <TableCell sx={{ fontWeight: "bold" }}>S.No</TableCell>
        <TableCell sx={{ fontWeight: "bold" }}>UserName</TableCell>
        <TableCell sx={{ fontWeight: "bold" }}>Leave-Type</TableCell>
        <TableCell sx={{ fontWeight: "bold" }}>Start-Date</TableCell>
        <TableCell sx={{ fontWeight: "bold" }}>End-Date</TableCell>
        <TableCell sx={{ fontWeight: "bold" }}>Total-Days</TableCell>
        <TableCell sx={{ fontWeight: "bold" }}>Status</TableCell>
        <TableCell sx={{ fontWeight: "bold" }}>Action</TableCell>

            </TableRow>
          </TableHead>

          <TableBody>
            {defaultLeaveData.map((row, index) => (
              <TableRow key={row.id}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{row.username}</TableCell>
                <TableCell>{row.leaveType}</TableCell>
                <TableCell>{row.startDate}</TableCell>
                <TableCell>{row.endDate}</TableCell>
                <TableCell sx={{ textAlign: "center"}}>{row.totalDays}</TableCell>
                <TableCell>
                  <Chip
                    label={row.status}
                    color={
                      row.status === "Approved"
                        ? "success"
                        : row.status === "Rejected"
                        ? "error"
                        : "warning"
                    }
                  />
                </TableCell>
                <TableCell>
                  <IconButton
                    color="primary"
                      aria-label="edit user"
                    onClick={() => {
                      setSelectedUserForStatus(row);
                     
                      setStatusModalOpen(true);
                    }}
                  >
                    <EditIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* STATUS UPDATE MODAL */}
      {selectedUserForStatus && (
        <Dialog
          open={statusModalOpen}
          onClose={() => setStatusModalOpen(false)}
          PaperProps={{ sx: { width: 400, borderRadius: 2 } }}
        >
          <DialogTitle sx={{ textAlign: "center", fontWeight: "bold" }}>
            Update Status
          </DialogTitle>

          <DialogContent  sx={{ px: 4, py: 2, display: "flex", flexDirection: "column", gap: 3 }}>
            <FormControl fullWidth margin="dense">
              <InputLabel>Status</InputLabel>
              <Select label="Status">
                <MenuItem value="Approved">Approved</MenuItem>
                <MenuItem value="Rejected">Rejected</MenuItem>
              </Select>
            </FormControl>
          </DialogContent>

          <DialogActions>
            <Button onClick={() => setStatusModalOpen(false)}>Cancel</Button>
            <Button>
              Save
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </Box>
  );
};

export default UserLeaveList;
