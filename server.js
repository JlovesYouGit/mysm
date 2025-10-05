const express = require('express');
const cors = require('cors');
const crypto = require('crypto');
const app = express();
const port = 8082; // Changed from 8083 to 8082 to match the PowerShell script

const jwtSecret = 'CHANGE_THIS_SECRET_KEY_IN_PRODUCTION';

function base64urlEncode(str) {
  return Buffer.from(str).toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

function base64urlToBase64(str) {
  let base64 = str.replace(/-/g, '+').replace(/_/g, '/');
  while (base64.length % 4) {
    base64 += '=';
  }
  return base64;
}

function generateJWT(userId) {
  const header = base64urlEncode(JSON.stringify({alg: 'HS256', typ: 'JWT'}));
  const payload = base64urlEncode(JSON.stringify({user_id: userId, exp: Math.floor(Date.now() / 1000) + 3600}));
  const signature = base64urlEncode(crypto.createHmac('sha256', jwtSecret).update(`${header}.${payload}`).digest('base64'));
  return `${header}.${payload}.${signature}`;
}

function verifyJWT(token) {
  const parts = token.split('.');
  if (parts.length !== 3) return false;
  const expectedSignature = base64urlEncode(crypto.createHmac('sha256', jwtSecret).update(`${parts[0]}.${parts[1]}`).digest('base64'));
  if (expectedSignature !== parts[2]) return false;
  const payload = JSON.parse(Buffer.from(base64urlToBase64(parts[1]), 'base64').toString());
  return payload.exp > Math.floor(Date.now() / 1000) ? payload : false;
}

function authMiddleware(req, res, next) {
  // Temporarily disable auth for testing
  next();
  /*
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({detail: 'Invalid token'});
  }
  const token = authHeader.substring(7);
  const payload = verifyJWT(token);
  if (!payload) {
    return res.status(401).json({detail: 'Invalid token'});
  }
  req.user = payload;
  next();
  */
}

app.use(cors());
app.use(express.json());

// Mock data
let numbers = [
  { id: '1', number: '+18506577838', country: 'United States', country_code: '+1', status: 'assigned', user_id: 'admin' }
];

let availableNumbers = [];
for (let i = 0; i < 10; i++) {
  availableNumbers.push({
    id: `avail_${i}`,
    number: `+1${Math.floor(Math.random() * 900 + 200)}${Math.floor(Math.random() * 900 + 100)}${Math.floor(Math.random() * 9000 + 1000)}`,
    country: 'United States',
    country_code: '+1',
    status: 'available'
  });
}

// Auth
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  if (username === 'admin' && password === 'telecom2025') {
    const token = generateJWT('admin');
    res.json({ token, success: true });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

// Numbers
app.get('/api/numbers', authMiddleware, (req, res) => {
  res.json({ numbers });
});

app.get('/api/numbers/available', authMiddleware, (req, res) => {
  res.json({ numbers: availableNumbers });
});

app.post('/api/numbers/assign', authMiddleware, (req, res) => {
  const { number } = req.body;
  const available = availableNumbers.find(n => n.number === number);
  if (available) {
    numbers.push({ ...available, status: 'assigned', user_id: 'admin' });
    availableNumbers = availableNumbers.filter(n => n.number !== number);
    res.json({ success: true });
  } else {
    res.status(400).json({ error: 'Number not available' });
  }
});

// SMS
app.post('/api/sms/send', authMiddleware, (req, res) => {
  res.json({ success: true, message_id: 'msg_' + Date.now() });
});

app.get('/api/sms/messages', authMiddleware, (req, res) => {
  res.json({ messages: [] });
});

// Voice
app.post('/api/voice/call', authMiddleware, (req, res) => {
  res.json({ success: true, call_id: 'call_' + Date.now() });
});

app.get('/api/voice/calls', authMiddleware, (req, res) => {
  res.json({ calls: [] });
});

// Spectrum
app.get('/api/spectrum/towers', authMiddleware, (req, res) => {
  res.json({
    towers: [
      { id: 1, name: 'Tower A', frequency: '850MHz', signal: -75, location: '34.0522° N, 118.2437° W' },
      { id: 2, name: 'Tower B', frequency: '1900MHz', signal: -82, location: '40.7128° N, 74.0060° W' }
    ]
  });
});

app.get('/api/spectrum/status', authMiddleware, (req, res) => {
  res.json({ status: 'active', last_scan: Date.now() - 300000 });
});

app.post('/api/spectrum/scan', authMiddleware, (req, res) => {
  res.json({ status: 'scanning', message: 'Spectrum scan initiated' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: Date.now() });
});

app.listen(port, () => {
  console.log(`Express API running at http://localhost:${port}`);
});