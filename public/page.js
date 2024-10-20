document.getElementById('checkButton').addEventListener('click', async () => {
    const password = document.getElementById('password').value;

    // Check if the password input is not empty
    if (!password) {
        document.getElementById('result').innerText = "Please enter a password.";
        return;
    }

    // Reset strength display before fetching
    const strengthDisplay = document.getElementById('strengthDisplay');
    const strengthLevel = document.getElementById('strengthLevel');

    // Set initial width to 0 and show the display
    strengthLevel.style.width = '0%'; 
    strengthDisplay.style.display = 'block'; 

    // Simulate a delay for visual effect
    await new Promise(resolve => setTimeout(resolve, 100));

    // Fetch password strength
    const response = await fetch('http://localhost:5000/check_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password })
    });

    if (!response.ok) {
        document.getElementById('result').innerText = "Error in processing the password.";
        return;
    }

    const result = await response.json();
    updateStrengthDisplay(result.strength); // Update strength display with the received strength
});

function updateStrengthDisplay(strength) {
    const strengthDisplay = document.getElementById('strengthDisplay');
    const strengthLevel = document.getElementById('strengthLevel');

    // Reset styles
    strengthLevel.style.width = '0%';
    strengthLevel.className = 'strength-level'; // Reset class

    // Show the display
    strengthDisplay.style.display = 'block';

    // Adding a timeout for the sliding effect
    setTimeout(() => {
        switch (strength.toLowerCase()) {
            case 'weak':
                strengthLevel.style.width = '33%';
                strengthLevel.classList.add('weak');
                break;
            case 'medium':
                strengthLevel.style.width = '66%';
                strengthLevel.classList.add('medium');
                break;
            case 'strong':
                strengthLevel.style.width = '100%';
                strengthLevel.classList.add('strong');
                break;
            default:
                strengthLevel.style.width = '0%'; // Default to 0%
                break;
        }
    }, 500); // Delay to allow the 0% to show first
}