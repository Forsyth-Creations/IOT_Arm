"use client";

import { Login } from '@mui/icons-material';
import HeartbeatBar from '../../comps/HeartbeatBars';
import LoginRedirect from '@/comps/LoginRedirect';
import * as React from 'react';
import ResponsiveAppBar from '@/comps/ResponsiveAppBar';

import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import LoadingButton from '@mui/lab/LoadingButton';
import CheckIcon from '@mui/icons-material/Check';

import axios from 'axios';

import Cookies from 'js-cookie';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 12,
  p: 4,
};

export default function Console() {

  // 26 characters

  const [openModal, setOpenModal] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
  const [disabled, setDisabled] = React.useState(true);
  const [heldValue, setHeldValue] = React.useState("");
  const [buttonText, setButtonText] = React.useState("Register Device");

  const [showCheck, setShowCheck] = React.useState(false);

  const handleOpenModal = () => {
    setOpenModal(true);
  }

  const handleCloseModal = () => {
    setOpenModal(false);
    setHeldValue("");
    setButtonText("Register Device");
    setDisabled(true);
  }

  const handleHeldValue = (event : any) => {
    setHeldValue(event.target.value);
    if (event.target.value.length >= 36) {
      console.log("Enabled")
      setDisabled(false);
      setLoading(true);

      // Make an API request to see if the device exists
      axios.get('http://localhost:8000/api/v1/device/' + event.target.value)
      .then(function (response) {
        console.log(response);
        if (response.status == 200) {
          setDisabled(false);
          setLoading(false);
          setButtonText("Register Device");
          // timeout
          setShowCheck(true);
          setTimeout(() => {
            setShowCheck(false);
          }, 400);
        }
      }
      )
      .catch(function (error) {
        setDisabled(true);
        setLoading(false);
        setButtonText(error.response.data.detail);
      }
      );

    } 
    else {
      console.log("Register Device")
      setDisabled(true);
      setLoading(false);
      setButtonText("Register Device");
    }
  }

  const RegisterDevice = () => {
    console.log("Registering device");
    axios.post('http://localhost:8000/api/v1/registerDevice', {
      uid: heldValue,
      token: Cookies.get('token')
    })
      .then(function (response) {
        console.log(response);        
        setButtonText("Device Registered");
        setDisabled(true);
      })
      .catch(function (error) {
        console.log(error);
        setButtonText(error.response.data.detail);
        setDisabled(true);
      });
  }

  return (
    <LoginRedirect>
      <Box>
        <ResponsiveAppBar></ResponsiveAppBar>
        <Container>
          <Stack direction="row"
            justifyContent="space-between">
            <h1>Device List</h1>
            <Button onClick={handleOpenModal}>Register Device</Button>
          </Stack>
          <HeartbeatBar></HeartbeatBar>
        </Container>
        <div>
          <Modal
            open={openModal}
            onClose={handleCloseModal}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
          >
            <Box sx={style}>
              <FormControl fullWidth>
                <TextField id="outlined-basic" label="Device UID" variant="outlined" 
                value={heldValue}
                onChange={handleHeldValue}/>
                <LoadingButton
                  size="small"
                  loading={loading}
                  variant="outlined"
                  disabled={disabled}
                  onClick={RegisterDevice}
                >
                  {!showCheck ? 
                  <Typography>{buttonText}</Typography>:
                  <CheckIcon></CheckIcon>}
                </LoadingButton>
              </FormControl>
            </Box>
          </Modal>
        </div>
      </Box>
    </LoginRedirect>
  );
};