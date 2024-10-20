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

// Usage example
(async () => {
  try {
    const password = 'your_password';
    const strength = await getStrength(password);
    console.log('Strength:', strength); // Should print "weak", "medium", or "strong"
  } catch (err) {
    console.error('Error:', err);
  }
})();