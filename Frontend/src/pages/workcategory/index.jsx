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
    Box,
    IconButton,
    Typography,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    CircularProgress,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { addWorkCategory, getWorkCategory, editWorkCategory } from "@/api/allApi";
import Pagination from "@/components/Pagination";



export default function WorkCategory() {
    const [search, setSearch] = useState("");
    const [tasks, setTasks] = useState([]);
    const [open, setOpen] = useState(false);
    const [editMode, setEditMode] = useState(false);
    const [selectedTask, setSelectedTask] = useState(null);
    const [loading, setLoading] = useState(false);
    const [tableLoading, setTableLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const usersPerPage = 10;
    const navigate = useNavigate();

    //  Fetch categories when page loads
    
    useEffect(() => {
        const delayDebounce = setTimeout(() => {
            fetchCategories();
        }, 400); // debounce API call (400ms delay)
        return () => clearTimeout(delayDebounce);
    }, [currentPage, search]); // refetch on page or search change

    useEffect(() => {
        setCurrentPage(1);
    }, [search]);


    const fetchCategories = async () => {
        try {
            setTableLoading(true);
            const res = await getWorkCategory(currentPage, search);

            // Map API data to internal structure
            if (res) {
                setTasks(
                    res?.results.map((item) => ({
                        id: item.id,
                        uuid: item.uuid,
                        category: item.identity || "-",
                    })) || []
                );
                const total = res.count
                    ? Math.ceil(res.count / 10)
                    : (res.total_pages || 1);

                setTotalPages(total);

            } else {
                setTasks([]);
                setTotalPages(1);
            }

        } catch (error) {
            console.error(error);
            toast.error("Error fetching categories");
        } finally {
            setTableLoading(false);
        }
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };


    // Filter tasks
    // const filteredTasks = tasks.filter((task) =>
    //     task.category?.toLowerCase().includes(search.toLowerCase())
    // );

    // Open popup for Add / Edit
    const handleOpen = (task = null) => {
        if (task) {
            setEditMode(true);
            setSelectedTask(task);
        } else {
            setEditMode(false);
            setSelectedTask({ category: "" });
        }
        setOpen(true);
    };

    const handleClose = () => setOpen(false);

    const handleSave = async () => {
        try {
            if (!selectedTask?.category.trim()) {
                toast.error("Category name is required!");
                return;
            }

            setLoading(true);

            if (editMode) {
                //  Update existing category
                const payload = { identity: selectedTask.category };
                const res = await editWorkCategory(selectedTask.id, payload); //  use id here
                toast.success("Category updated successfully!");
                await fetchCategories();
            } else {
                //  Add new via API
                const payload = { identity: selectedTask.category };
                const res = await addWorkCategory(payload);
                toast.success("Category added successfully!");
                await fetchCategories(); //  Refetch data after add
                // if (res) {
                // } else {
                //     toast.error("Failed to add category");
                // }
            }

            setOpen(false);
        } catch (error) {
            console.error("Error saving category:", error);
            toast.error("Something went wrong!");
        } finally {
            setLoading(false);
        }
    };


    return (
        <Box sx={{ p: 3 }}>
            {/* Top bar */}
            <Box
                sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    mb: 2,
                }}
            >
                <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                    Project List
                </Typography>

                <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                    <TextField
                        variant="outlined"
                        size="small"
                        label="Search Category"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />

                    <Button
                        variant="contained"
                        color="primary"
                        startIcon={<AddIcon />}
                        onClick={() => handleOpen()}
                    >
                        Add Project
                    </Button>
                </Box>
            </Box>

            {/* Table */}
            <TableContainer component={Paper}>
                {tableLoading ? (
                    <Box sx={{ p: 3, textAlign: "center" }}>
                        <CircularProgress />
                    </Box>
                ) : (
                    <Table sx={{ minWidth: 650 }} aria-label="task table">
                        <TableHead>
                            <TableRow>
                                <TableCell sx={{ fontWeight: "bold" }}>S.No</TableCell>
                                <TableCell sx={{ fontWeight: "bold" }}>Category</TableCell>
                                <TableCell sx={{ fontWeight: "bold" }}>Action</TableCell>
                            </TableRow>
                        </TableHead>

                        <TableBody>
                            {tasks.length > 0 ? (
                                tasks.map((task, index) => (
                                    <TableRow key={task.uuid}>
                                        {/* <TableCell>{index + 1}</TableCell> */}
                                        <TableCell>{(currentPage - 1) * usersPerPage + index + 1}</TableCell>
                                        <TableCell>{task.category || "-"}</TableCell>
                                        <TableCell>
                                            <IconButton
                                                color="secondary"
                                                onClick={() => handleOpen(task)}
                                            >
                                                <EditIcon />
                                            </IconButton>
                                        </TableCell>
                                    </TableRow>
                                ))
                            ) : (
                                <TableRow>
                                    <TableCell colSpan={3} align="center">
                                        No categories found.
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                )}
            </TableContainer>

            {/*  Dialog for Add/Edit */}
            <Dialog
                open={open}
                onClose={handleClose}
                fullWidth
                maxWidth="sm"
                sx={{
                    "& .MuiDialog-paper": {
                        position: "absolute",
                        top: 20,
                        margin: 0,
                    },
                }}
            >
                <DialogTitle>
                    {editMode ? "Edit Category" : "Add Category"}
                </DialogTitle>
                <DialogContent
                    sx={{ px: 4, py: 2, display: "flex", flexDirection: "column", gap: 3 }}
                >
                    <TextField
                        label="Category"
                        value={selectedTask?.category || ""}
                        onChange={(e) =>
                            setSelectedTask({
                                ...selectedTask,
                                category: e.target.value,
                            })
                        }
                        fullWidth
                        margin="dense"
                    />
                </DialogContent>

                <DialogActions>
                    <Button onClick={handleClose}>Cancel</Button>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleSave}
                        disabled={loading}
                    >
                        {loading
                            ? "Saving..."
                            : editMode
                                ? "Update"
                                : "Add"}
                    </Button>
                </DialogActions>
            </Dialog>

            <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
                maxVisiblePages={3}
            />
        </Box>
    );
}
