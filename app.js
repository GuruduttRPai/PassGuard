const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { PythonShell } = require('python-shell');
const path = require('path'); // Import path module

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public'))); // Serve static files from the public folder

const { spawn } = require('child_process');

async function getStrength(password) {
  const pythonProcess = spawn('python', ['py_main.py', password]);

  return new Promise((resolve, reject) => {
    let output = '';
    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Error running Python script:', data.toString());
      reject(new Error('Error running Python script'));
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        resolve(output.trim()); // Extract the strength value (single line)
      } else {
        reject(new Error('Python script exited with error code:', code));
      }
    });
  });
}



// Serve the HTML page
app.get('/home', async (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'page.html'));
});







app.post('/check_password', async (req, res) => {
  const { password } = req.body;

  if (!password) {
    return res.status(400).send('Password is required');
  }

  console.log("About to run Python script with password:", password);

  try {
    const strength = await getStrength(password);
    console.log('strength: ', strength); // This will print the strength

    if (strength === 'error') {
      return res.status(500).send('error');
    }

    // Send the response immediately after getting the strength
    return res.status(200).json({ 'strength': strength });
  } catch (err) {
    console.error('Error:', err);
    return res.status(500).send('error');
  }
});


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
