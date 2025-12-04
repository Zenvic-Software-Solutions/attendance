import React, { useEffect, useState } from "react";
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
} from "@mui/material";
import {
  ArrowBack,
  Person,
  Email,
  LocationOn,
  Phone,
  Work,
  Cake,
  Business,
  CheckCircle,
  Cancel,
} from "@mui/icons-material";
import { getUserDetails } from "@/api/allApi";
import toast from "react-hot-toast";
import { useNavigate, useParams } from "react-router-dom"; 

export default function UserDetailsCard() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { uuid } = useParams(); //  get uuid from route params

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const response = await getUserDetails(uuid); //  pass uuid here
      if (response) {
        setUser(response || {});
      } else {
        toast.error("No user data found!");
        setUser({});
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
      toast.error("Failed to load user details.");
      setUser({});
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (uuid) {
      fetchUserData();
    } else {
      toast.error("No user ID provided in URL!");
    }
  }, [uuid]);

  if (loading) {
    return (
      <Box
        sx={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (!user) {
    return (
      <Box
        sx={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Typography variant="h6" color="text.secondary">
          No user details available
        </Typography>
      </Box>
    );
  }

  const isActive =
    user?.is_active === true ||
    user?.status?.toLowerCase() === "active" ||
    user?.status === 1;

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "flex-start",
        alignItems: "flex-start",
        p: 3,
      }}
    >
      <Card
        sx={{
          width: "95%",
          maxWidth: 1200,
          borderRadius: 3,
          boxShadow: "0 6px 20px rgba(0,0,0,0.08)",
          overflow: "hidden",
        }}
      >
        {/* Header */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            p: 3,
            borderBottom: "1px solid #E5E7EB",
          }}
        >
          <Typography variant="h6" fontWeight="bold">
            User Details
          </Typography>
          <Button
            variant="contained"
            startIcon={<ArrowBack />}
            onClick={() => navigate(-1)}
            sx={{
              textTransform: "none",
              backgroundColor: "#3B82F6",
              "&:hover": { backgroundColor: "#2563EB" },
            }}
          >
            Back
          </Button>
        </Box>

        {/* Content */}
        <CardContent sx={{ p: 4 }}>
          <Grid container spacing={3}>
            {/* Name */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="subtitle2" mb={1}>
                Name
              </Typography>
              <TextField
                fullWidth
                value={user.identity || ""}
                InputProps={{
                  startAdornment: <Person sx={{ color: "gray", mr: 1 }} />,
                  readOnly: true,
                }}
                sx={{ backgroundColor: "#ECEFF1", borderRadius: 1 }}
              />
            </Grid>

            {/* Email */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="subtitle2" mb={1}>
                Email
              </Typography>
              <TextField
                fullWidth
                value={user.email || ""}
                InputProps={{
                  startAdornment: <Email sx={{ color: "gray", mr: 1 }} />,
                  readOnly: true,
                }}
                sx={{ backgroundColor: "#ECEFF1", borderRadius: 1 }}
              />
            </Grid>

            {/* Phone */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="subtitle2" mb={1}>
                Phone
              </Typography>
              <TextField
                fullWidth
                value={user.phone_number || ""}
                InputProps={{
                  startAdornment: <Phone sx={{ color: "gray", mr: 1 }} />,
                  readOnly: true,
                }}
                sx={{ backgroundColor: "#ECEFF1", borderRadius: 1 }}
              />
            </Grid>

            {/* DOB */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="subtitle2" mb={1}>
                Date of Birth
              </Typography>
              <TextField
                fullWidth
                value={user.dob || ""}
                InputProps={{
                  startAdornment: <Cake sx={{ color: "gray", mr: 1 }} />,
                  readOnly: true,
                }}
                sx={{ backgroundColor: "#ECEFF1", borderRadius: 1 }}
              />
            </Grid>

            {/* City */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="subtitle2" mb={1}>
                City
              </Typography>
              <TextField
                fullWidth
                value={user.city || ""}
                InputProps={{
                  startAdornment: <Business sx={{ color: "gray", mr: 1 }} />,
                  readOnly: true,
                }}
                sx={{ backgroundColor: "#ECEFF1", borderRadius: 1 }}
              />
            </Grid>

            {/* Domain */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="subtitle2" mb={1}>
                Domain
              </Typography>
              <TextField
                fullWidth
                value={user.domain || ""}
                InputProps={{
                  startAdornment: <Work sx={{ color: "gray", mr: 1 }} />,
                  readOnly: true,
                }}
                sx={{ backgroundColor: "#ECEFF1", borderRadius: 1 }}
              />
            </Grid>

            {/* Gender */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="subtitle2" mb={1}>
                Gender
              </Typography>
              <RadioGroup row value={user.gender || ""}>
                <FormControlLabel
                  value="Male"
                  control={<Radio disabled sx={{
                    color: "#1976d2", 
                    "&.Mui-checked": { color: "#1976d2" }, 
                  }} />}
                  label="Male"
                />
                <FormControlLabel
                  value="Female"
                  control={<Radio disabled sx={{
                    color: "#1976d2",
                    "&.Mui-checked": { color: "#1976d2" },
                  }} />}
                  label="Female"
                />
              </RadioGroup>
            </Grid>

            {/* Address */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="subtitle2" mb={1}>
                Address
              </Typography>
              <TextField
                fullWidth
                multiline
                minRows={3}
                value={user.address || ""}
                InputProps={{
                  startAdornment: (
                    <LocationOn sx={{ color: "gray", mr: 1, mt: 0.5 }} />
                  ),
                  readOnly: true,
                }}
                sx={{
                  backgroundColor: "#ECEFF1",
                  borderRadius: 1,
                }}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
}
