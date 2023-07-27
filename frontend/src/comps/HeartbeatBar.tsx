"use client";

import { useEffect, useState } from 'react';

import { AiFillHeart } from 'react-icons/ai';
import { FaExclamationTriangle } from 'react-icons/fa';
import { IoPencil, IoCheckmark } from 'react-icons/io5';
import { Accordion, AccordionSummary, AccordionDetails, Typography } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';

import axios from 'axios';

import GenericModal from './GenericModal';

export default function HeartbeatBar(props: { uid: string, timestamp: number, data: JSON }) {

  // see if the timestamp is older than 5 seconds
  // if it is, show a warning
  // if it isn't, show a heartbeat
  const [isOpen, setIsOpen] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [restartInProgress, setRestartInProgress] = useState(false);
  const [nameEdit, setNameEdit] = useState(false);
  const [name, setName] = useState('');


  // Pull the name from the api based on the UID
  useEffect(() => {
    axios.get('http://0.0.0.0:8000/api/v1/getName/' + props.uid, {
    })
      .then(function (response) {
        console.log(response);
        setName(response.data.name);
      })
      .catch(function (error) {
        console.log(error);
        setName(props.uid);
      });
  }, [props.uid, setName]);

  const openModal = () => {
    setShowModal(true);
  };

  const handleDropdownToggle = () => {
    setIsOpen(!isOpen);
  };


  const handleSubmit = () => {
    console.log("Submitting name change");
    axios.post('http://0.0.0.0:8000/api/v1/assignName', {
      uid: props.uid,
      name: name
    })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  // Make a class to the backend to toggle an LED
  const toggleLED = () => {
    console.log("Toggling LED");
    axios.post('http://0.0.0.0:8000/api/v1/toggleLED', {
      uid: props.uid
    })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  const handleRestart = () => {
    console.log("Restarting device");
    setIsStale(true);
    setRestartInProgress(true);
    axios.post('http://0.0.0.0:8000/api/v1/restart', {
      uid: props.uid
    })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  const handleGetHealthData = () => {
    console.log("Getting health data");
    axios.post('http://0.0.0.0:8000/api/v1/health', {
      uid: props.uid
    })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  const [isStale, setIsStale] = useState<boolean>(false);

  // Write a useeffect that refreshes every 5 seconds
  // if the timestamp is older than 5 seconds, set isStale to true
  function padZero(value: number) {
    return value < 10 ? `0${value}` : value;
  }

  const now = new Date(props.timestamp);
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const seconds = now.getSeconds();
  // get date
  const date = now.getDate();
  const month = now.getMonth() + 1;
  const year = now.getFullYear();
  const formattedTime = `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)} ${padZero(date)}/${padZero(month)}/${year}`;

  // Set a timeout. When the timeout is reached, set restartInProgress to false
  useEffect(() => {
    if (restartInProgress) {
      setTimeout(() => {
        setRestartInProgress(false);
      }, 10000);
    }
  }, [restartInProgress, setRestartInProgress]);

  // every few seconds, check if the timestamp is older than 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const secondsSinceLastUpdate = (now.getTime() - props.timestamp) / 1000;
      if (secondsSinceLastUpdate > 8) {
        setIsStale(true);
      } else {
        setIsStale(false);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [props.timestamp, setIsStale, setRestartInProgress]);


  return (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography>
          <div>{name}</div>
          <Typography sx={{ color: 'text.secondary', alignItems: "center", display : "flex" }}>
          Last Seen: {formattedTime}
          {isStale ? (
            <FaExclamationTriangle color="red" style = {{marginLeft : "10px"}}></FaExclamationTriangle>
          ) : (
            <AiFillHeart color="maroon" style = {{marginLeft : "10px"}}></AiFillHeart>
          )}
          </Typography>
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Typography >
          {restartInProgress && <Typography className="text-yellow-600">Admin commanded restart... Standby</Typography>}

          { nameEdit ? 
          <Typography>Name: 
            <input type = "text" value = {name} onChange = {(e) => setName(e.target.value)}>
              </input>
              <IoCheckmark onClick = {() => {setNameEdit(false); handleSubmit();}}></IoCheckmark></Typography> : 
          <Typography>Name: {name}<IoPencil onClick = {() => setNameEdit(true)}></IoPencil></Typography> 
          }
          <Typography>UID: {props.uid}</Typography>
          <Typography>Timestamp: {formattedTime}</Typography>
          <Typography>Data:</Typography>
          <Typography>
          {props.data && Object.entries(props.data).map(([key, value]) => {
            return (
              <div key={key}
                className="flex flex-row">
                <Typography>{key} - {value}</Typography>
              </div>
            );
          })}
          </Typography>
          <Button variant="contained" onClick={openModal} className="p-2 bg-blue-400 rounded mt-3 text-xs hover:bg-blue-500">Command</Button>
        </Typography>
      </AccordionDetails>
      <GenericModal showModal={showModal} setShowModal={setShowModal} className="">
        <div className="flex flex-row">
          <Button variant="contained" onClick={toggleLED} className="m-2 p-2 bg-blue-400 rounded mt-3 text-xs hover:bg-blue-500">Toggle LED</Button>
          <Button variant="contained" onClick={handleRestart} className="m-2 p-2 bg-red-400 rounded mt-3 text-xs hover:bg-red-500">Restart</Button>
          <Button variant="contained" onClick={handleGetHealthData} className="m-2 p-2 bg-green-400 rounded mt-3 text-xs hover:bg-green-500">Get Health Data</Button>
        </div>
      </GenericModal>
    </Accordion>
  );
};