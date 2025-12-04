import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
} from "@mui/material";

const LogoutModal = ({ open, onCancel, onConfirm }) => {
  return (
    <Dialog
      open={open}
      onClose={onCancel}
      aria-labelledby="logout-dialog-title"
      PaperProps={{
        sx: {
          borderRadius: "12px",
          p: 2,
          textAlign: "center",
          width: 350,
        },
      }}
    >
      {/* Red warning icon */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          mb: 1,
        }}
      >
        <Box
          sx={{
            backgroundColor: "#f44336",
            borderRadius: "50%",
            width: 50,
            height: 50,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Typography
            variant="h5"
            sx={{ color: "white", fontWeight: "bold", lineHeight: 1 }}
          >
            !
          </Typography>
        </Box>
      </Box>

      {/* Title */}
      <DialogTitle
        id="logout-dialog-title"
        sx={{ fontWeight: 700, textAlign: "center", pb: 0 }}
      >
        Confirm Logout
      </DialogTitle>

      {/* Subtitle */}
      <DialogContent sx={{ textAlign: "center", color: "#555", pt: 1 }}>
        Are you sure you want to Logout?
      </DialogContent>

      {/* Action Buttons */}
      <DialogActions
        sx={{
          justifyContent: "center",
          pb: 2,
          gap: 2,
        }}
      >
        <Button
          onClick={onCancel}
          variant="contained"
          sx={{
            backgroundColor: "#f44336",
            "&:hover": { backgroundColor: "#d32f2f" },
            color: "white",
            fontWeight: 600,
            borderRadius: "8px",
            px: 3,
          }}
        >
          CANCEL
        </Button>
        <Button
          onClick={onConfirm}
          variant="contained"
          sx={{
            backgroundColor: "#1976d2",
            "&:hover": { backgroundColor: "#1565c0" },
            color: "white",
            fontWeight: 600,
            borderRadius: "8px",
            px: 3,
          }}
        >
          LOGOUT
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default LogoutModal;
