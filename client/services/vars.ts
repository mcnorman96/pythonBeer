import { io } from 'socket.io-client';

// Use environment variable or default to localhost
export const API_URL = process.env.API_URL || 'http://localhost:8000';
export const socket = io(API_URL); // Flask-SocketIO default port
