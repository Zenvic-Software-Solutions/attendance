import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  Button,
  Box,
  IconButton,
  Typography,
  Chip,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import { useNavigate } from "react-router-dom";
import { getUserList, updateUserStatus } from "@/api/allApi";
import Pagination from "@/components/Pagination";
import EditStatusModal from "@/components/EditStatusModal";
import toast from "react-hot-toast";

export default function Index() {
  const [search, setSearch] = useState("");
  const [users, setUsers] = useState([]);
  const [statusModalOpen, setStatusModalOpen] = useState(false);
  const [selectedUserForStatus, setSelectedUserForStatus] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const usersPerPage = 10;
  const navigate = useNavigate();

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
      const response = await getUserList(currentPage, search);
      if (response) {
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

  return (
    <Box sx={{ p: 3 }}>
      {/* Top bar: Search + Add Button */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Typography variant="h6" sx={{ fontWeight: "bold" }}>
          User List
        </Typography>

        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          <TextField
            variant="outlined"
            size="small"
            label="Search User"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </Box>
      </Box>

      {/* Table */}
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold" }}>S.No</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Name</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Phone</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Email</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Gender</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Domain</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Active</TableCell>
              <TableCell sx={{ fontWeight: "bold" }}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.length > 0 ? (
              users.map((user, index) => (
                <TableRow key={user.uuid}>
                  <TableCell>
                    {(currentPage - 1) * usersPerPage + index + 1}
                  </TableCell>
                  <TableCell>{user.identity || "-"}</TableCell>
                  <TableCell>{user.phone_number || "-"}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.gender}</TableCell>
                  <TableCell>{user.domain || "-"}</TableCell>
                  <TableCell>
                    <Chip
                      label={user.is_active ? "Active" : "Inactive"}
                      color={user.is_active ? "success" : "error"}
                      size="small"
                    />
                  </TableCell>

                  <TableCell>
                    <IconButton
                      color="primary"
                      aria-label="edit user"
                      onClick={() => {
                        setSelectedUserForStatus(user);
                        setStatusModalOpen(true);
                      }}
                    >
                      <EditIcon />
                    </IconButton>

                    <IconButton
                      color="primary"
                      onClick={() => handleView(`${user.uuid}`)}
                      aria-label="view user"
                    >
                      <VisibilityIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={8} align="center">
                  No matching users found.
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

      <EditStatusModal
        open={statusModalOpen}
        currentStatus={selectedUserForStatus?.is_active ? "active" : "inactive"}
        currentMode={selectedUserForStatus?.mode || "online"}
        onClose={() => setStatusModalOpen(false)}
        onSave={async ({ status, mode }) => {
          try {
            const payload = {
              is_active: status === "active" ? "true" : "false",
              mode: mode === "online" ? "false" : "true",
            };

            const res = await updateUserStatus(
              selectedUserForStatus.uuid,
              payload
            );

            toast.success(res?.message || "User updated successfully");

            // Update UI instantly
            setUsers((prev) =>
              prev.map((u) =>
                u.uuid === selectedUserForStatus.uuid
                  ? {
                      ...u,
                      is_active: status === "active",
                      mode: mode,
                    }
                  : u
              )
            );

            setStatusModalOpen(false);
          } catch (error) {
            toast.error("Failed to update user");
            console.error(error);
          }
        }}
      />
    </Box>
  );
}
