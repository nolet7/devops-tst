import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from frontend directory
app.use(express.static(join(__dirname, 'frontend')));

// API endpoints
app.get('/api/info', (req, res) => {
  res.json({
    version: "1.0.0",
    environment: process.env.NODE_ENV || "development",
    endpoints: [
      "/api/info",
      "/api/submit",
      "/healthz"
    ]
  });
});

app.post('/api/submit', (req, res) => {
  const { message } = req.body;
  
  if (!message) {
    return res.status(400).json({ error: "Message is required" });
  }
  
  // Echo back the message with some processing
  res.json({
    status: "success",
    received_message: message,
    processed_at: new Date().toISOString(),
    response: `Processed: ${message}`
  });
});

app.get('/healthz', (req, res) => {
  res.json({ status: "healthy", timestamp: new Date().toISOString() });
});

// Serve the main HTML file for root path
app.get('/', (req, res) => {
  res.sendFile(join(__dirname, 'frontend', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});