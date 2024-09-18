document.addEventListener('DOMContentLoaded', () => {
    const formBlock = document.getElementById('block-form');

    const authForm = document.getElementById('auth-form');
    const nicknameInput = document.getElementById('nickname');
    const checkNicknameButton = document.getElementById('check-nickname');

    const registerForm = document.getElementById('register-form');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const registerButton = document.getElementById('register');

    const loginForm = document.getElementById('login-form');
    const loginPasswordInput = document.getElementById('login-password');
    const loginButton = document.getElementById('login');

    const authForm2 = document.getElementById('auth-form2');
    const nicknameInput2 = document.getElementById('nickname2');
    const checkNicknameButton2 = document.getElementById('check-nickname2');

    const registerForm2 = document.getElementById('register-form2');
    const passwordInput2 = document.getElementById('password2');
    const confirmPasswordInput2 = document.getElementById('confirm-password2');
    const registerButton2 = document.getElementById('register2');

    const loginForm2 = document.getElementById('login-form2');
    const loginPasswordInput2 = document.getElementById('login-password2');
    const loginButton2 = document.getElementById('login2');

    const gameContainer = document.getElementById('game1');
    const tournamentContainer = document.getElementById('tournament-bracket');

    const burgerMenu = document.querySelector('.navbar');

    const pongElements = document.getElementById('pong-elements');
    const logo = document.querySelector('.logo');

    const postFormButtons = document.getElementById('post-form-buttons');
    const localGameButton = document.getElementById('local-game');
    const quickMatchButton = document.getElementById('quick-match');
    const tournamentButton = document.getElementById('tournament');

    let socket;
    let token;
    let gameState;
    let saveData = null;

    // Auto-focus and key handling for AUTH-FORM
    nicknameInput.focus();
    nicknameInput.addEventListener('keypress', function (event) {
        history.pushState({ view: 'auth-form' }, '', `#${'auth-form'}`);
        if (event.key === 'Enter') {
            event.preventDefault();
            checkNicknameButton.click();
        }
    });

    checkNicknameButton.addEventListener('click', handleCheckNickname);
    registerButton.addEventListener('click', handleRegister);
    loginButton.addEventListener('click', handleLogin);

    checkNicknameButton2.addEventListener('click', handleCheckNickname2);
    registerButton2.addEventListener('click', handleRegister2);
    loginButton2.addEventListener('click', handleLogin2);

    localGameButton.addEventListener('click', startLocalGame);
    quickMatchButton.addEventListener('click', startQuickMatch);
    tournamentButton.addEventListener('click', startTournament);

    async function handleCheckNickname() {
        const nickname = nicknameInput.value.trim();
        if (nickname) {
            window.firstPlayerName = nickname;
            try {
                const exists = await checkUserExists(nickname);
                if (exists) {
                    authForm.style.display = 'none';
                    loginForm.style.display = 'block';
                    loginPasswordInput.focus();
                    loginPasswordInput.addEventListener('keypress', function (event) {
                        if (event.key === 'Enter') {
                            event.preventDefault();
                            loginButton.click();
                        }
                    });
                } else {
                    authForm.style.display = 'none';
                    registerForm.style.display = 'block';
                    passwordInput.focus();
                    passwordInput.addEventListener('keypress', function (event) {
                        if (event.key === 'Enter') {
                            confirmPasswordInput.focus();
                            confirmPasswordInput.addEventListener('keypress', function (event) {
                                if (event.key === 'Enter') {
                                    event.preventDefault();
                                    registerButton.click();
                                }
                            });
                        }
                    });
                }
            } catch (error) {
                console.error('Error checking user existence:', error);
            }
        } else {
            alert('Please enter a nickname.');
        }
    }

    async function checkUserExists(username) {
        const response = await fetch('/check_user_exists/', {
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
                    document.getElementById("post-form-buttons").style.display = 'block';
                    history.pushState({ view: 'post-form-buttons' }, '', `#${'post-form-buttons'}`);
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
        const response = await fetch('/register_user/', {
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
                document.getElementById("post-form-buttons").style.display = 'block';
                history.pushState({ view: 'post-form-buttons' }, '', `#${'post-form-buttons'}`);
                burgerMenu.style.display = 'block';
                logo.style.display = 'none';
                pongElements.style.display = 'none';        
            } else {
                alert('Authentication failed. Please try again.');
            }
        } catch (error) {
            console.error('Error authenticating user:', error);
        }
    }

    async function authenticateUser(username, password) {
        const response = await fetch('/authenticate_user/', {
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

    async function handleCheckNickname2() {
        const nickname2 = nicknameInput2.value.trim();
        if (nickname2) {
            try {
                const exists = await checkUserExists2(nickname2);
                if (exists) {
                    authForm2.style.display = 'none';
                    loginForm2.style.display = 'block';
                    loginPasswordInput2.focus();
                    loginPasswordInput2.addEventListener('keypress', function (event) {
                        if (event.key === 'Enter') {
                            event.preventDefault();
                            loginButton2.click();
                        }
                    });
                } else {
                    authForm2.style.display = 'none';
                    registerForm2.style.display = 'block';
                    passwordInput2.focus();
                    passwordInput2.addEventListener('keypress', function (event) {
                        if (event.key === 'Enter') {
                            confirmPasswordInput2.focus();
                            confirmPasswordInput2.addEventListener('keypress', function (event) {
                                if (event.key === 'Enter') {
                                    event.preventDefault();
                                    registerButton2.click();
                                }
                            });
                        }
                    });
                }
            } catch (error) {
                console.error('Error checking user existence:', error);
            }
        } else {
            alert('Please enter a nickname.');
        }
    }

    async function checkUserExists2(username) {
        const response = await fetch('/check_user_exists/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username })
        });
        const data = await response.json();
        return data.exists;
    }

    async function handleRegister2() {
        const nickname2 = nicknameInput2.value.trim();
        const password2 = passwordInput2.value.trim();
        const confirmPassword2 = confirmPasswordInput2.value.trim();

        if (password2 === confirmPassword2) {
            try {
                const result = await registerUser2(nickname2, password2);
                if (result) {
                    registerForm2.style.display = 'none';
                    startLocalGame2();
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

    async function registerUser2(username, password) {
        const response = await fetch('/register_user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (data.registered) {
            token2 = data.token;
        }
        return data.registered;
    }

    async function handleLogin2() {
        const nickname2 = nicknameInput2.value.trim();
        const password2 = loginPasswordInput2.value.trim();
        try {
            const result = await authenticateUser2(nickname2, password2);
            if (result) {
                loginForm2.style.display = 'none';
                startLocalGame2();
            } else {
                alert('Authentication failed. Please try again.');
            }
        } catch (error) {
            console.error('Error authenticating user:', error);
        }
    }

    async function authenticateUser2(username, password) {
        const response = await fetch('/authenticate_user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (data.authenticated) {
            token2 = data.token;
        }
        return data.authenticated;
    }

    function startLocalGame() {
        console.log("starting a Local Game..");
        document.getElementById("post-form-buttons").style.display = 'none';
        authForm2.style.display = 'block';
        nicknameInput2.focus();
        nicknameInput2.addEventListener('keypress', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                checkNicknameButton2.click();
            }
        });
    }

    function startLocalGame2() {
        nickname = nicknameInput.value.trim();
        nickname2 = nicknameInput2.value.trim();
        saveData = {
            type: 'local',
            player1_name: nickname,
            player2_name: nickname2
        };
        gameContainer.style.display = 'flex';
        formBlock.style.display = 'none';
        startWebSocketConnection(token, 2);
    }

    function startQuickMatch() {
        saveData = {
            type: 'quick'
        }
        gameContainer.style.display = 'flex';
        formBlock.style.display = 'none';
        document.getElementById('player1-name').textContent = "player 1";
        document.getElementById('player2-name').textContent = "player 2";
        document.getElementById('game-text').textContent = "";
        document.getElementById('player1-score').textContent = 0;
        document.getElementById('player2-score').textContent = 0;

        startWebSocketConnection(token, 1);
    }

    function startTournament() {
        saveData = {
            type: 'tournoi'
        }
        tournamentContainer.style.display = 'flex';
        formBlock.style.display = 'none';
        startWebSocketConnection(token, 42);
    }

    function startWebSocketConnection(token, players) {
        history.pushState({ view: 'game1' }, '', `#${'game1'}`);
        console.log("view local");
        socket = new WebSocket(`wss://${window.location.host}/ws/game/`);

        socket.onopen = function (event) {
            console.log('WebSocket connection established');
            if (players === 1) {
                console.log("Sending token for a quick match game");
                socket.send(JSON.stringify({ type: 'authenticate', token: token }));
               /*  history.pushState({ view: 'game1' }, '', `#${'game1'}`);
                console.log("view quick"); */
            } else if (players === 2) {
                console.log("Sending tokens for a local game");
                socket.send(JSON.stringify({ type: 'authenticate2', token_1: token, token_2: token2 }));
                /* history.pushState({ view: 'game1' }, '', `#${'game1'}`);
                console.log("view local"); */
            } else {
                console.log("Sending token for a tournament game")
                socket.send(JSON.stringify({ type: 'authenticate3', token: token }));
                /* history.pushState({ view: 'game1' }, '', `#${'game1'}`);
                console.log("view tournament"); */
            }
        };

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (data.type === 'authenticated') {
                console.log('Authentication successful');
            } else if (data.type === 'waiting_room') {
                console.log('Entered the WAITING ROOM');
            } else if (data.type === 'game_start') {
                console.log('Game started:', data.game_id, '(', data.player1, 'vs', data.player2, ')');
                gameContainer.style.display = 'flex';
                document.addEventListener('keydown', handleKeyDown);
            } else if (data.type === 'game_state_update') {
                updateGameState(data.game_state);
            } else if (data.type === 'game_text_update') {
                updateGameText(data.game_text);
            } else if (data.type === 'player_disconnected') {
                console.log('Player disconnected:', data.player);
            } else if (data.type === 'game_ended') {
                console.log('Game ended:', data.game_id);
            } else if (data.type === 'error') {
                console.error(data.message);
            } else if (data.type === 'update_tournament_waiting_room') {
                // Update the HTML content of the tournament bracket
                tournamentContainer.innerHTML = data.html;
                // Reattach the event listener to the "Start Tournament" button
                const startButton = document.getElementById('start-tournament-btn');
                if (startButton) {
                    startButton.addEventListener('click', function() {
                        if (typeof socket !== 'undefined' && socket.readyState === WebSocket.OPEN) {
                            console.log('Start TOURNAMENT sent..');
                            socket.send(JSON.stringify({type: 'start_tournament'}));
                        } else {
                            console.error('WebSocket is not open or undefined');
                        }
                    });
                }
            } else if (data.type === 'update_brackets') {
                // Update the HTML content of the tournament bracket
                tournamentContainer.innerHTML = data.html;
            } else if (data.type === 'tournament_end') {
                console.log('Tournament ended, the winner is:', data.winner);
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

    function handleKeyDown(event) {
        if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'w' || event.key === 's') {
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
        checkForWinner();
    }

    function renderGame() {
        document.getElementById('player1-name').textContent = `${gameState.player1_name}`;
        document.getElementById('player2-name').textContent = `${gameState.player2_name}`;

        document.getElementById('player1-pad').style.top = `${gameState.player1_position}px`;
        document.getElementById('player2-pad').style.top = `${gameState.player2_position}px`;

        document.getElementById('ball').style.left = `${gameState.ball_position.x}px`;
        document.getElementById('ball').style.top = `${gameState.ball_position.y}px`;

        document.getElementById('player1-score').textContent = gameState.player1_score;
        document.getElementById('player2-score').textContent = gameState.player2_score;

        document.getElementById('game-text').textContent = gameState.game_text;
    }

    function updateGameText(gameText) {
        document.getElementById('game-text').textContent = gameText;
    }

    const starsContainer = document.getElementById('stars');
    for (let i = 0; i < 500; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = `${Math.random() * 3}px`;
        star.style.height = star.style.width;
        star.style.left = `${Math.random() * 100}%`;
        star.style.top = `${Math.random() * 100}%`;
        star.style.animationDuration = `${Math.random() * 2 + 1}s`;
        starsContainer.appendChild(star);
    }

    const homeButton = document.getElementById('home');
    const replayButton = document.getElementById('retry');
    const gameControls = document.getElementById('game-controls');

    homeButton.addEventListener('click', () => {
        gameContainer.style.display = 'none';
        gameControls.style.display = 'none';
        formBlock.style.display = 'block';
        postFormButtons.style.display = 'block';
        history.pushState({ view: 'post-form-buttons' }, '', `#${'post-form-buttons'}`);
    
        setupFirstPlayer();
    });

    function setupFirstPlayer() {
        const firstPlayerName = window.firstPlayerName; 
        document.getElementById('player1-name').textContent = firstPlayerName;
    }

    replayButton.addEventListener('click', () => {
        document.getElementById('player1-name').textContent = saveData.player1_name;
        document.getElementById('player2-name').textContent = saveData.player2_name;
        startLocalGame2();
    });

    function checkForWinner() {
        if (gameState.player1_score === 3 || gameState.player2_score === 3) {
            if (saveData.type != "tournoi"){
                if (gameContainer.style.display != 'none'){
                    gameControls.style.display = 'flex';
                    homeButton.style.display = 'block';
                    replayButton.style.display = 'none';
                    console.log(saveData.type);
                    if (saveData.type === 'local'){
                        replayButton.style.display = 'block';
                    }
                }
            }
        }
    }

    const initialView = window.location.hash ? window.location.hash.substring(1) : 'auth-form';

    // Écouteur pour les boutons de retour et d'avance du navigateur
    window.addEventListener('popstate', (event) => {
        const view = event.state ? event.state.view : 'auth-form'; // Utilise l'état sauvegardé
        showSection(view);
    });

    const sections = {
        'auth-form': authForm,
        'register-form': registerForm,
        'login-form': loginForm,
        'post-form-buttons': postFormButtons,
        'game1': gameContainer,
        'auth-form2': authForm2,
        'register-form2': registerForm2,
        'login-form2': loginForm2
    };

    function showSection(viewId) {
        Object.values(sections).forEach(section => {
            section.style.display = 'none';
        });
        console.log(viewId);
        const sectionToShow = sections[viewId];
        console.log(sectionToShow);
        if (sectionToShow) {
            if (viewId == 'auth-form' || viewId == 'post-form-buttons'){
                console.log("here");
                formBlock.style.display = 'block';
            } else {
                formBlock.style.display = 'none'
            }
            sectionToShow.style.display = 'block';
        } else {
            console.error(`La section avec l'ID "${viewId}" n'a pas été trouvée.`);
        }
    }

});
