"use client";

import { useEffect } from 'react';
import Cookies from 'js-cookie';
import { ReactElement } from 'react';
import Box from '@mui/material/Box';

interface LoginRedirectProps {
    children: ReactElement<any, any>;
    redirectUrl?: string; // Optional prop for the redirect URL
  }

export default function LoginRedirect({ children, redirectUrl = "" }: LoginRedirectProps) {
    useEffect(() => {
        // Function to handle redirection based on the token
        const handleRedirect = () => {
          const token = Cookies.get('token');
          if (token === undefined) {
            window.location.href = '/login';
          }
          else if (redirectUrl !== "")
          {
            window.location.href = redirectUrl;
          }
        };
        handleRedirect(); // Call the handleRedirect function on mount
      }, []); // Empty dependency array ensures it runs only once after initial mount    
    
    return (
        <Box sx={{flexGrow : 1, minHeight : "100vh"}}>
            {children}
        </Box>
    )
}
