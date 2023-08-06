"use client";

import { useEffect, useState } from 'react';
import socket from '../context/socket';
import HeartbeatBar from './HeartbeatBar';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Typography } from '@mui/material';
import LinearProgress from '@mui/material/LinearProgress';

// This component will occassionally be fed new data from it's parent
// when this data does stale, it needs to show a warning
// when this data is fresh, it needs to show a heartbeat

export default function HeartbeatBars() {
    // create a dictionary of uid's and elements
    const [uidElementMap, setUidElementMap] = useState<Map<string, JSX.Element>>(new Map());
    const [uidList, setUidList] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);

    // useEffect(() => {

    //     const handleMessage = (data: string) => {
    //         // Parse the data as json
    //         var message = JSON.parse(data);

    //         var now = new Date();
    //         var newTimestamp = now.getTime();
            
    //         // set the mapping of uid to element
    //         setUidElementMap((uidElementMap) => {
    //             const newMap = new Map(uidElementMap);
    //             newMap.set(message.uid, <HeartbeatBar key={message.uid} data = {message.data} uid={message.uid} timestamp={newTimestamp}></HeartbeatBar>);
    //             return newMap;
    //         }
    //         );

    //         // Generate the elements based on the map. But the elements must be HeatbeatBar
    //         // elements, not just JSX elements

    //     };

    //     socket.addMessageHandler(handleMessage);

    //     return () => {
    //         socket.removeMessageHandler(handleMessage);
    //     };
    // }, []);

    var myToken = Cookies.get('token');

    // Make an axios call to get the uid list of devices
    useEffect(() => {
        axios.post('http://localhost:8000/api/v1/devices/', {
            token : myToken
        })
        .then(function (response) {
            console.log(response);
            if (response.status == 200) {
                // set the mapping of uid to element
                setUidElementMap((uidElementMap) => {
                    const newMap = new Map(uidElementMap);
                    var now = new Date();
                    var newTimestamp = now.getTime();
                    setUidList(response.data.devices)
                    for (var i = 0; i < response.data.devices.length; i++) {
                        var myUID = response.data.devices[i];
                        newMap.set(myUID, <HeartbeatBar key={myUID} uid={myUID} timestamp={newTimestamp}></HeartbeatBar>);
                    }
                    return newMap;
                }
                );
            }
            setLoading(false);
        }
        )
        .catch(function (error) {
            console.log(error);
        }
        );
    }, []);


    return (
        <div className="flex flex-col">
            {loading && <LinearProgress />}
            {uidList.length > 0 && Array.from(uidElementMap.values())}
            {uidList.length == 0 && !loading && <Typography variant="h6">No devices registered. Please register above</Typography>}
        </div>
    );
}
