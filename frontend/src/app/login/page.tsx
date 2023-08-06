"use client";

import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import FavoriteIcon from '@mui/icons-material/Favorite';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from 'axios';
import Alert from '@mui/material/Alert';
import Cookies from 'js-cookie';
import { redirect } from 'next/navigation';
import { WindowRounded } from '@mui/icons-material';


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

export default function SignIn() {

  const [showError, setShowError] = React.useState(false);
  const [showRemeberMeNote, setShowRemeberMeNote] = React.useState(false);

  const alert = (message: string) => {
    console.log(message);
    setShowError(true);
    // Set a timeout to hide the alert again
    setTimeout(() => {
      setShowError(false);
    }
    , 5000);
  };

  const handleRememberMe = (event: React.ChangeEvent<HTMLInputElement>) => {
    setShowRemeberMeNote(event.target.checked);
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    
    axios.post('http://localhost:8000/api/v1/login', {
      email: data.get('email'),
      password: data.get('password'),
    })
      .then(function (response) {
        console.log(response);
        // Store the token in a cookie
        // TODO: set the cookie to expire after 2 days
        if (showRemeberMeNote)
        {
          Cookies.set('token', response.data.token, { expires: 7 });
        }
        else
        {
          Cookies.set('token', response.data.token, { expires: 1 });
        }
      })
      .then(function (response) {
        // Redirect to the console, redirect with window.location.href
        window.location.href = '/console';
      })
      .catch(function (error) {
        console.log(error);
        alert('Login failed');
      });
  };

  return (
      <Container maxWidth="xs"  sx={{minHeight : "100vh"}}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            paddingTop : "12vh"
          }}
        >
          <Avatar sx={{ bgcolor: 'secondary.main' }}>
            <FavoriteIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" onClick = {handleRememberMe}/>}
              label="Remember me for 7 days"
            />
            {showError && <Alert severity="error">Login failed. Please try again</Alert>}
            {showRemeberMeNote && <Alert severity="info">Note: Credentials will be saved for 7 days</Alert>}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link href="/create_account" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 8, mb: 4 }} />
      </Container>
  );
}