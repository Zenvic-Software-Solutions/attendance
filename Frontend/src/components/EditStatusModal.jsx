import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";

const EditStatusModal = ({ open, onClose, currentStatus, currentMode, onSave }) => {
  const [status, setStatus] = useState(currentStatus);
  const [mode, setMode] = useState(currentMode);

  React.useEffect(() => {
    setStatus(currentStatus);
    setMode(currentMode);
  }, [currentStatus, currentMode]);

  return (
    <Dialog
      open={open}
      onClose={onClose}
      disableScrollLock
      PaperProps={{
        sx: {
          width: 400,
          borderRadius: 3,
          p: 1,
        },
      }}
    >
      <DialogTitle sx={{ textAlign: "center", fontWeight: "bold" }}>
        Edit User Status
      </DialogTitle>

      <DialogContent
        sx={{ px: 4, py: 2, display: "flex", flexDirection: "column", gap: 3 }}
      >
        <FormControl fullWidth margin="dense">
          <InputLabel>Status</InputLabel>
          <Select
            value={status}
            label="Status"
            onChange={(e) => setStatus(e.target.value)}
          >
            <MenuItem value="active">Active</MenuItem>
            <MenuItem value="inactive">Inactive</MenuItem>
          </Select>
        </FormControl>

        {/* MODE DROPDOWN */}
        <FormControl fullWidth margin="dense">
          <InputLabel>Mode</InputLabel>
          <Select
            value={mode}
            label="Mode"
            onChange={(e) => setMode(e.target.value)}
          >
            <MenuItem value="online">Online</MenuItem>
            <MenuItem value="offline">Offline</MenuItem>
          </Select>
        </FormControl>
      </DialogContent>

    

      <DialogActions sx={{ justifyContent: "space-between", px: 3, pb: 2 }}>
        <Button onClick={onClose} sx={{ color: "gray", fontWeight: "bold" }}>
          Cancel
        </Button>

        <Button
          variant="contained"
          onClick={() => onSave(status)}
          sx={{ px: 3, fontWeight: "bold", borderRadius: 2 }}
        >
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditStatusModal;
