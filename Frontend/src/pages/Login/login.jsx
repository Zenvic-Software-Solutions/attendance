import React, { useState } from "react";
import {
    Box,
    Card,
    CardContent,
    TextField,
    IconButton,
    InputAdornment,
    Typography,
    Button,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import toast from "react-hot-toast";
import { login } from "@/api/allApi";
import { useNavigate } from "react-router-dom";



const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("")
    const [showPassword, setShowPassword] = useState(false);
    const [errors, setErrors] = useState({ email: "", password: "" });

    const navigate = useNavigate();

    const handleTogglePassword = () => {
        setShowPassword(!showPassword)
    }

    const handleLogin = async () => {

        let tempErrors = { email: "", password: "" }
        let isValid = true;

        // Email validation
        if (!email.trim()) {
            tempErrors.email = " Email is required";
            isValid = false;
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            tempErrors.email = " Enter a valid email address";
            isValid = false;
        }

        // Password validation
        if (!password.trim()) {
            tempErrors.password = " Password is required";
            isValid = false;
        } else if (password.trim().length < 4) {
            tempErrors.password = " Password must be at least 4 characters";
            isValid = false;
        }

        setErrors(tempErrors);

        if (isValid) {
            try {
                const res = await login({ email, password });

                console.log(res);

                toast.success("Login Successful");
                localStorage.setItem("token", res?.token)

                // Reset fields
                setEmail("");
                setPassword("");
                setErrors({ email: "", password: "" });
                navigate("/dashboard");

            } catch (error) {
                console.error(error);
                toast.error(error.response?.data?.message || "Login failed. Try again.");
            }
        }
    }


    return (
        <Box
            sx={{
                height: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                backgroundColor: "#f5f5f5",
                position: "relative",
                overflow: "hidden",

                // put the before/after on this outer Box
                "&::before, &::after": {
                    content: '""',
                    position: "absolute",
                    width: 239,
                    height: 234,
                    backgroundImage: `url("data:image/svg+xml,%3Csvg width='239' height='234' viewBox='0 0 239 234' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='88.5605' y='0.700195' width='149' height='149' rx='19.5' stroke='%237367F0' stroke-opacity='0.16'/%3E%3Crect x='0.621094' y='33.761' width='200' height='200' rx='10' fill='%237367F0' fill-opacity='0.08'/%3E%3C/svg%3E")`,
                    backgroundRepeat: "no-repeat",
                    backgroundSize: "contain",
                    zIndex: 0,
                    "@media (max-width:600px)": {
                        display: "none",
                    },
                },
                "&::before": {
                    top: "15%",
                    left: "10%",
                },
                "&::after": {
                    bottom: "10%",
                    right: "15%",
                },
            }}
        >
            <Card
                variant="outlined"
                sx={{
                    position: "relative",
                    maxWidth: 400,
                    width: "100%",
                    p: 3,
                    boxShadow: 3,
                    borderRadius: 3,
                    backgroundColor: "#fff",
                    zIndex: 1, // ensures card sits ABOVE the background shapes
                }}
            >
                <CardContent sx={{ position: "relative", zIndex: 2 }} >
                    <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
                        <img
                            src="/logo/logo.png"
                            alt="Zenvic Software Solutions"
                            style={{ width: "175px", height: "auto" }}
                        />
                    </Box>

                    {/* Title */}
                    <Typography
                        variant="h5"
                        component="div"
                        sx={{ textAlign: "center", fontWeight: "bold", mb: 3 }}
                    >
                        Zenvic Attendance Login
                    </Typography>
                    <Typography
                        variant="p"
                        component="div"
                        sx={{ textAlign: "center", fontSize: 17, mb: 3 }}
                    >
                        Please sign in to your account
                    </Typography>
                    {/* Email Field */}
                    <form
                        onSubmit={(e) => {
                            e.preventDefault(); // prevent page reload
                            handleLogin();
                        }}
                    >
                        <TextField
                            fullWidth
                            label="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            error={!!errors.email} // !! -> mui error expect boolean so "!!" is used to convert any value to boolean
                            helperText={errors.email}
                            variant="outlined"
                            margin="normal"
                            sx={{
                                "& .MuiInputLabel-root.Mui-focused": {
                                    color: "#c649ff", // label color when focused
                                },
                                "& .MuiOutlinedInput-root": {
                                    "&:hover fieldset": {
                                        borderColor: "black",
                                    },
                                    "&.Mui-focused fieldset": {
                                        borderColor: "#c649ff",
                                    },
                                    // "&.Mui-focused .MuiInputBase-input": {
                                    //     color: "#c649ff", 
                                    // },
                                },
                            }}
                        />

                        {/* Password Field */}
                        <TextField
                            fullWidth
                            label="Password"
                            type={showPassword ? "text" : "password"}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            error={!!errors.password}
                            helperText={errors.password}
                            variant="outlined"
                            margin="normal"
                            InputProps={{
                                endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton onClick={handleTogglePassword} edge="end">
                                            {showPassword ? <VisibilityOff /> : <Visibility />}
                                        </IconButton>
                                    </InputAdornment>
                                )
                            }}
                            sx={{
                                "& .MuiInputLabel-root.Mui-focused": {
                                    color: "#c649ff", // label color when focused
                                },
                                "& .MuiOutlinedInput-root": {
                                    "&:hover fieldset": {
                                        borderColor: "black",
                                    },
                                    "&.Mui-focused fieldset": {
                                        borderColor: "#c649ff",
                                    },
                                    // "&.Mui-focused .MuiInputBase-input": {
                                    //     color: "#c649ff",
                                    // },
                                },
                            }}
                        />

                        {/* Login Button */}
                        <Button
                            variant="contained"
                            type="submit"
                            fullWidth
                            sx={{
                                color: "#fff",
                                backgroundColor: "#c649ff",
                                borderColor: "#c649ff"
                            }}
                        >
                            Login
                        </Button>
                    </form>
                    {/* Extra Text */}
                    <Typography
                        variant="body2"
                        sx={{ textAlign: "center", mt: 2, color: "text.secondary" }}
                    >
                        Forgot Password?
                    </Typography>
                </CardContent>
            </Card>
        </Box>
    );
};

export default Login;
