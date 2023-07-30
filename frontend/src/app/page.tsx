import React from 'react';
import { Container, Grid, Typography } from '@mui/material';
import HeartbeatBars from '../comps/HeartbeatBars';

// Connect to my socket
// and listen for messages

export default function MyPageComponent() {
  return (
    <Container maxWidth={false} sx={{ height: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'left', padding: "1rem" }}>
      <Typography variant="h3" gutterBottom>
        Health Monitor
      </Typography>
      <Grid container>
        <HeartbeatBars />
      </Grid>
    </Container>
  );
}
