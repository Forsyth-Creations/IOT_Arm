"use client";

import HeartbeatBar from '../comps/HeartbeatBars';

// Connect to my socket
// and listen for messages

export default function MyPageComponent() {

  return (
    <main className="flex min-h-screen flex-col p-8">
      <h1>Health Monitor</h1>
      <HeartbeatBar></HeartbeatBar>
    </main>
  );
};