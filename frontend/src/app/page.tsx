"use client";

import { useEffect } from 'react';
// import { redirect } from 'next/navigation';
import Cookies from 'js-cookie';

// MUI loading
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import LoginRedirect from '@/comps/LoginRedirect';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';

export default function MyPageComponent() {

  return (
    <main>
      <LoginRedirect redirectUrl="/console">
        <Container sx={{minHeight:"100vh"}}>
          <Stack sx={{display: "flex", 
          justifyContent: "center", 
          alignItems: "center",
          paddingTop : "12vh"}}>
          <Typography>Loading Health Monitor</Typography>
          <CircularProgress />
          </Stack>
        </Container>
      </LoginRedirect>
    </main>
  );
}
