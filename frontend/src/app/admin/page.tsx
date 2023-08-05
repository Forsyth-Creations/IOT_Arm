// A list of styled links to the admin pages

import React from 'react';

// Use mui buttons
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';

// Nextjs link
import Link from 'next/link';




export default function Admin() {
    return (
        <Container component="main" maxWidth="xs" sx = {{display : "flex"}}>
            <Button sx = {{margin: "4px"}} href="/apiDocs" variant="contained">API Docs</Button>
            <Button sx = {{margin: "4px"}} href="http://localhost:8001/" variant="contained">Database Admin</Button>
        </Container>
    );
}

