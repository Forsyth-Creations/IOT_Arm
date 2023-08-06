"use client";

import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import FavoriteIcon from '@mui/icons-material/Favorite';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from 'axios';

// Import link for nextjs
// https://nextjs.org/docs/api-reference/next/link
import Link from 'next/link';


// Checkmark from mui
// https://mui.com/components/material-icons/
import CheckIcon from '@mui/icons-material/Check';

function Copyright(props: any) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://www.forsythcreations.com">
        Forsyth Creations LLC
      </Link>{' '}
      {new Date().getFullYear()}
    </Typography>
  );
}

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function SignUp() {

  const [showComplete, setShowComplete] = React.useState(false);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log("------------ Data --------------");
    // get the json from all keys in data
    const json = Object.fromEntries(data.entries());

    axios.post('http://localhost:8000/api/v1/create_account', {
      data: json
    })
      .then(function (response) {
        console.log(response);
        setShowComplete(true);
      })
      .catch(function (error) {
        console.log(error);
        alert('Account creation failed: ' + error.response.data.detail);
      });
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container 
      component="main" 
      maxWidth="xs" 
      style = {{minHeight : "100vh"}}>
        {!showComplete &&
          <Box
            sx={{
              paddingTop: "10px",
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
              <FavoriteIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign up
            </Typography>
            <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete="given-name"
                    name="firstName"
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    autoFocus
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    name="lastName"
                    autoComplete="family-name"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="new-password"
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        name="allowExtraEmails"
                        id="allowExtraEmails"
                        value="allowExtraEmails"
                        color="primary" />}
                    label="I want to receive inspiration, marketing promotions and updates via email."
                  />
                </Grid>
              </Grid>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign Up
              </Button>
              <Grid container justifyContent="center">
                  <Link href="/login">
                    Already have an account? Sign in
                  </Link>
              </Grid>
            </Box>
          </Box>}
        {showComplete &&
          <Box
            sx={{
              paddingTop: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography component="h1" variant="h5">Welcome to the party!</Typography>
            <CheckIcon></CheckIcon>
            <Button component = {Link} href="/login">Go to login</Button>
          </Box>}
        <Copyright sx={{ mt: 5 }} />
      </Container>
    </ThemeProvider>
  );
}