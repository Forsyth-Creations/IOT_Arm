"use client";

import { useEffect } from 'react';
// import { redirect } from 'next/navigation';
import Cookies from 'js-cookie';

// MUI loading
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import LoginRedirect from '@/comps/LoginRedirect';

export default function MyPageComponent() {

  return (
    <main>
      <LoginRedirect redirectUrl="/console">
        <Container>
          <Typography>Loading Health Monitor<CircularProgress /></Typography>
        </Container>
      </LoginRedirect>
    </main>
  );
}
