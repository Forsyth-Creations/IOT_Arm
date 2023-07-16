"use client";

import { useEffect, useState } from 'react';
import socket from '../context/socket';
import HeartbeatBar from './HeartbeatBar';

// This component will occassionally be fed new data from it's parent
// when this data does stale, it needs to show a warning
// when this data is fresh, it needs to show a heartbeat

import { AiFillHeart } from 'react-icons/ai';

export default function HeartbeatBars() {
    // create a dictionary of uid's and elements
    const [uidElementMap, setUidElementMap] = useState<Map<string, JSX.Element>>(new Map());

    useEffect(() => {

        const handleMessage = (data: string) => {
            // Parse the data as json
            var message = JSON.parse(data);

            var now = new Date();
            var newTimestamp = now.getTime();
            
            // set the mapping of uid to element
            setUidElementMap((uidElementMap) => {
                const newMap = new Map(uidElementMap);
                newMap.set(message.uid, <HeartbeatBar data = {message.data} uid={message.uid} timestamp={newTimestamp}></HeartbeatBar>);
                return newMap;
            }
            );

            // Generate the elements based on the map. But the elements must be HeatbeatBar
            // elements, not just JSX elements

        };

        socket.addMessageHandler(handleMessage);

        return () => {
            socket.removeMessageHandler(handleMessage);
        };
    }, []);

    return (
        <div className="flex flex-col">
            {Array.from(uidElementMap.values())}
        </div>
    );
}
