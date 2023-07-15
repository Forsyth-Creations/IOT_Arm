"use client";

import { useEffect, useState } from 'react';

import { AiFillHeart } from 'react-icons/ai';
import { FaExclamationTriangle } from 'react-icons/fa';

export default function HeartbeatBar( props: { uid: string, timestamp: number}) {

    // see if the timestamp is older than 5 seconds
    // if it is, show a warning
    // if it isn't, show a heartbeat
    const [isOpen, setIsOpen] = useState(false);

    const handleDropdownToggle = () => {
        setIsOpen(!isOpen);
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

    // every few seconds, check if the timestamp is older than 5 seconds
    useEffect(() => {
        const interval = setInterval(() => {
            const now = new Date();
            const secondsSinceLastUpdate = (now.getTime() - props.timestamp) / 1000;
            console.log(secondsSinceLastUpdate)
            if (secondsSinceLastUpdate > 5) {
                setIsStale(true);
            } else {
                setIsStale(false);
            }
        }, 1000);
        return () => clearInterval(interval);
    }, [props.timestamp, setIsStale]);


return (
    <div className="dropdown flex flex-col justify-center">
      <div
        className={`min-width-80 flex flex-row justify-between align-middle bg-gray-300 p-4 border-2 rounded-md ${
          isOpen ? 'open' : ''
        }`}
        onClick={handleDropdownToggle}
      >
        <text className = "pointer-events-none">{props.uid}</text>
        <div className="flex flex-row items-center">
          <text className="text-xs pointer-events-none">Last Seen: {formattedTime}</text>
          <div className="p-2">
            {isStale ? (
              <FaExclamationTriangle color="red"></FaExclamationTriangle>
            ) : (
              <AiFillHeart color="maroon"></AiFillHeart>
            )}
          </div>
        </div>
      </div>
      {isOpen && (
        <div className="dropdown-content bg-slate-900 text-white w-11/12 p-4">
          <h1>UID: {props.uid}</h1>
          <h1>Timestamp: {formattedTime}</h1>
        </div>
      )}
    </div>
  );
};
