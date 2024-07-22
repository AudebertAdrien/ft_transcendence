document.addEventListener('DOMContentLoaded', () => {
    const checkNicknameButton = document.getElementById('check-nickname');
    const registerButton = document.getElementById('register');
    const loginButton = document.getElementById('login');
    const authForm = document.getElementById('auth-form');
    const gameContainer = document.getElementById('game1');
    const nicknameInput = document.getElementById('nickname');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const loginPasswordInput = document.getElementById('login-password');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    let socket;
    let token;
    let gameState;

    checkNicknameButton.addEventListener('click', handleCheckNickname);
    registerButton.addEventListener('click', handleRegister);
    loginButton.addEventListener('click', handleLogin);

    async function handleCheckNickname() {
        const nickname = nicknameInput.value.trim();
        if (nickname) {
            try {
                const exists = await checkUserExists(nickname);
                if (exists) {
                    authForm.style.display = 'none';
                    loginForm.style.display = 'block';
                } else {
                    authForm.style.display = 'none';
                    registerForm.style.display = 'block';
                }
            } catch (error) {
                console.error('Error checking user existence:', error);
            }
        } else {
            alert('Please enter a nickname.');
        }
    }

    async function checkUserExists(username) {
        const response = await fetch('/api/check_user_exists/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username })
        });
        const data = await response.json();
        return data.exists;
    }

    async function handleRegister() {
        const nickname = nicknameInput.value.trim();
        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();

        if (password === confirmPassword) {
            try {
                const result = await registerUser(nickname, password);
                if (result) {
                    registerForm.style.display = 'none';
                    gameContainer.style.display = 'flex';
                    startGame();
                } else {
                    alert('Registration failed. Please try again.');
                }
            } catch (error) {
                console.error('Error registering user:', error);
            }
        } else {
            alert('Passwords do not match.');
        }
    }

    async function registerUser(username, password) {
        const response = await fetch('/api/register_user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (data.registered) {
            token = data.token;
        }
        return data.registered;
    }

    async function handleLogin() {
        const nickname = nicknameInput.value.trim();
        const password = loginPasswordInput.value.trim();
        try {
            const result = await authenticateUser(nickname, password);
            if (result) {
                loginForm.style.display = 'none';
                gameContainer.style.display = 'flex';
                startWebSocketConnection(token);
            } else {
                alert('Authentication failed. Please try again.');
            }
        } catch (error) {
            console.error('Error authenticating user:', error);
        }
    }

    async function authenticateUser(username, password) {
        const response = await fetch('/api/authenticate_user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (data.authenticated) {
            token = data.token;
        }
        return data.authenticated;
    }

    function startWebSocketConnection(token) {
        socket = new WebSocket(`ws://${window.location.host}/ws/game/`);

        socket.onopen = function (event) {
            console.log('WebSocket connection established');
            socket.send(JSON.stringify({ type: 'authenticate', token: token }));
        };

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (data.type === 'authenticated') {
                console.log('Authentication successful');
            } else if (data.type === 'waiting_room') {
                console.log('Entered the waiting room');
            } else if (data.type === 'game_start') {
                console.log('Game started:', data.game_id, '(', data.player1, 'vs', data.player2, ')');
                startGame(data.game_id, data.player1, data.player2);
            } else if (data.type === 'game_state_update') {
                updateGameState(data.game_state);
            } else if (data.type === 'error') {
                console.error(data.message);
            } else {
                console.log('Message from server:', data.type, data.message);
            }
        };

        socket.onclose = function (event) {
            console.log('WebSocket connection closed');
        };

        socket.onerror = function (error) {
            console.error('WebSocket error:', error);
        };
    }

    function startGame(gameCode, player1_name, player2_name) {
        document.getElementById('gameCode').textContent = `Game Code: ${gameCode}`;
        document.getElementById('player1-name').textContent = `${player1_name}`;
        document.getElementById('player2-name').textContent = `${player2_name}`;
        document.addEventListener('keydown', handleKeyDown);
    }

    function handleKeyDown(event) {
        if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
            sendKeyPress(event.key.toLowerCase());
        }
    }

    function sendKeyPress(key) {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ type: 'key_press', key }));
        }
    }

    function updateGameState(newState) {
        gameState = newState;
        renderGame();
    }

    function renderGame() {
        const player1Pad = document.getElementById('player1-pad');
        player1Pad.style.top = `${gameState.player1_position}px`;

        const player2Pad = document.getElementById('player2-pad');
        player2Pad.style.top = `${gameState.player2_position}px`;

        const ball = document.getElementById('ball');
        ball.style.left = `${gameState.ball_position.x}px`;
        ball.style.top = `${gameState.ball_position.y}px`;

        const player1Score = document.getElementById('player1-score');
        player1Score.textContent = gameState.player1_score;

        const player2Score = document.getElementById('player2-score');
        player2Score.textContent = gameState.player2_score;
    }

});
