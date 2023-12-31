class WebSocketConnection {
  constructor(url) {
    this.url = url;
    this.socket = null;
    this.messageHandlers = [];
  }

  connect() {
    try {
      this.socket = new WebSocket(this.url);
      this.socket.onopen = this.handleOpen;
      this.socket.onmessage = this.handleMessage;
      this.socket.onclose = this.handleClose;
    } catch (error) {
      // Handle the error here
      console.error('Failed to connect:', error);
      // Optionally, you can trigger a callback or update the component state with the error information
    }
  }

  handleOpen = () => {
    console.log('WebSocket connection established.');
  };

  handleMessage = (event) => {
    this.messageHandlers.forEach((handler) => {
      handler(event.data);
    });
  };

  handleClose = () => {
    console.log('WebSocket connection closed.');
  };

  addMessageHandler(handler) {
    this.messageHandlers.push(handler);
  }

  removeMessageHandler(handler) {
    this.messageHandlers = this.messageHandlers.filter(
      (existingHandler) => existingHandler !== handler
    );
  }

  close() {
    this.socket.close();
  }
}

// generate a uid for each client
const uid = () => Math.random().toString(36).slice(2);
const socket = new WebSocketConnection('ws://localhost:8000/ws/' + uid());
socket.connect();

export default socket;
