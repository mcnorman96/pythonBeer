import { io, Socket } from 'socket.io-client';

export const API_URL: string = process.env.API_URL || 'http://localhost:8000';
export const socket: Socket = io(API_URL); // Flask-SocketIO default port
