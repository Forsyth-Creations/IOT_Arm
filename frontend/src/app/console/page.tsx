"use client";

import { Login } from '@mui/icons-material';
import HeartbeatBar from '../../comps/HeartbeatBars';
import LoginRedirect from '@/comps/LoginRedirect';
import * as React from 'react';
import ResponsiveAppBar from '@/comps/ResponsiveAppBar';

import Box from '@mui/material/Box';
import Container from '@mui/material/Container';

const pages = ['Products', 'Pricing', 'Blog'];
const settings = ['Profile', 'Account', 'Dashboard', 'Logout'];

export default function Console() {
  return (
      <LoginRedirect>
        <Box>
          <ResponsiveAppBar></ResponsiveAppBar>
          <Container>
            <h1>Health Monitor</h1>
            <HeartbeatBar></HeartbeatBar>
          </Container>
        </Box>
      </LoginRedirect>
  );
};