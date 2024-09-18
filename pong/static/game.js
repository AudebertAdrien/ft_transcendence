
document.addEventListener('DOMContentLoaded', () => {
	console.log("DOM fully loaded and parsed");
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

	const pongElements = document.getElementById('pong-elements');
	const logo = document.querySelector('.logo');

	const postFormButtons = document.getElementById('post-form-buttons');
	const localGameButton = document.getElementById('local-game');
	const quickMatchButton = document.getElementById('quick-match');
	const tournamentButton = document.getElementById('tournament');

	console.log("DOM elements initialized");

	// Auto-focus and key handling for AUTH-FORM
	nicknameInput.focus();
	nicknameInput.addEventListener('keypress', function (event) {
		if (event.key === 'Enter') {
			event.preventDefault();
			handleCheckNickname();  // Appeler directement la fonction au lieu de simuler un clic
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
	
	let socket;
	let gameState;
	let activeRoom = null;	// Stocker la room active
	let roomSockets = {}; // Stocker les connexions WebSocket par room
	let token = null;
	let username = null;
	let saveData = null;
	let roomName = null;
	let chatManager = null;
	

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
		console.log("checkUserExists called with username:", username);
		try {
			const response = await fetch('/check_user_exists/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ username })
			});
			if (!response.ok) {
				console.error(`HTTP error! Status: ${response.status}`);
				return false;
			}
			const data = await response.json();
			console.log("User existence check response:", data);
			return data.exists;
		} catch (error) {
			console.error('Error during user existence check:', error);
			return false;
		}
	}

	async function handleRegister() {
		console.log("handleRegister called");
		const nickname = nicknameInput.value.trim();
		const password = passwordInput.value.trim();
		const confirmPassword = confirmPasswordInput.value.trim();
		
		if (password === confirmPassword) {
			try {
				const result = await registerUser(nickname, password);
				if (result.registered) {
					token = result.token;
					console.log("Token stored:", token);
					console.log("User registered successfully");
					registerForm.style.display = 'none';
					document.getElementById("post-form-buttons").style.display = 'block';
					username = nickname;
					roomName = 'main_room';
					chatManager = new ChatManager(username, token);
					chatManager.joinRoom(roomName); // Utilisez ChatManager pour rejoindre la room
				} else {
					console.error('Registration failed. No token received.');
					alert('Registration failed. Please try again.');
				}
			} catch (error) {
				console.error('Error registering user:', error);
			}
		} else {
			alert('Passwords do not match.');
			console.error('Passwords do not match.');
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
			return { registered: true, token: data.token };
		} else {
			return { registered: false };
		}
	}

	async function handleLogin() {
		const nickname = nicknameInput.value.trim();
		const password = loginPasswordInput.value.trim();
		try {
			const result = await authenticateUser(nickname, password);
			if (result) {
				loginForm.style.display = 'none';
				document.getElementById("post-form-buttons").style.display = 'block';
				
				// Gérer la connexion WebSocket de chat
				if (chatManager && chatManager.roomSockets['main_room'] && chatManager.roomSockets['main_room'].readyState !== WebSocket.OPEN) {
					console.log('Rejoining chat room...');
					chatManager.startChatWebSocket('main_room');  // Relance la connexion WebSocket si nécessaire
				} else if (!chatManager) {
					username = nickname;
					console.log('Initializing ChatManager...');
					chatManager = new ChatManager(username, token); // Réinitialisation du ChatManager si nécessaire
					chatManager.joinRoom('main_room');
				}
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
		console.log("checkUserExists2 called with username:", username);
		try {
			const response = await fetch('/check_user_exists/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ username })
			});

			if (!response.ok) {
				console.error(`HTTP error! Status: ${response.status}`);
				return false;
			}
			const data = await response.json();
			console.log("User existence check response (checkUserExists2):", data);
			return data.exists;
		} catch (error) {
			console.error('Error during user existence check (checkUserExists2):', error);
			return false;
		}
	}

	async function handleRegister2() {
		console.log("handleRegister2 called");
		const nickname2 = nicknameInput2.value.trim();
		const password2 = passwordInput2.value.trim();
		const confirmPassword2 = confirmPasswordInput2.value.trim();
		
		if (password2 === confirmPassword2) {
			try {
				console.log("Attempting to register user (handleRegister2):", nickname2);
				const result = await registerUser2(nickname2, password2);
				if (result) {
					console.log("User registered successfully (handleRegister2)");
					registerForm2.style.display = 'none';
					startLocalGame2();
				} else {
					console.error('Registration failed (handleRegister2).');
					alert('Registration failed. Please try again.');
				}
			} catch (error) {
				console.error('Error registering user (handleRegister2):', error);
			}
		} else {
			alert('Passwords do not match.');
			console.error('Passwords do not match (handleRegister2).');
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
        logo.style.display = 'none';
        pongElements.style.display = 'none';
        formBlock.style.display = 'none';
        startWebSocketConnection(token, 2);
    }
	
	function startQuickMatch() {
		saveData = {
            type: 'quick'
        }
		console.log("Starting quick match...(fonction startquickmatch)");
		gameContainer.style.display = 'flex';
		logo.style.display = 'none';
		pongElements.style.display = 'none';
		formBlock.style.display = 'none';
		document.getElementById('player1-name').textContent = "player 1";
        document.getElementById('player2-name').textContent = "player 2";
        document.getElementById('game-text').textContent = "";
        document.getElementById('player1-score').textContent = 0;
        document.getElementById('player2-score').textContent = 0;
		chatManager = new ChatManager(username, token);	// Initialiser ChatManager
		chatManager.joinRoom('quick_match'); // ChatManager pour rejoindre la quick_match
		console.log("Starting WebSocket connection for quick match...");
		startWebSocketConnection(token, 1);
	}

	// Fonction pour démarrer un tournoi
	function startTournament() 
	{
		saveData = {
			type: 'tournoi'
		};
	tournamentContainer.style.display = 'flex';
	logo.style.display = 'none';
	pongElements.style.display = 'none';
	formBlock.style.display = 'none';
	chatManager = new ChatManager(username, token);
	chatManager.joinRoom('tournament'); // ChatManager pour rejoindre la tournament
	console.log("Starting WebSocket connection for tournament...");
	startWebSocketConnection(token, 42);
}

	function startWebSocketConnection(token, players) {
		if (socket && socket.readyState === WebSocket.OPEN) {
			socket.close();
		}
		socket = new WebSocket(`wss://${window.location.host}/ws/game/`);
		socket.onopen = function (event) {
			console.log('WebSocket connection established');
			if (players === 1) {
				socket.send(JSON.stringify({ type: 'authenticate', token: token }));
			} else if (players === 2) {
				socket.send(JSON.stringify({ type: 'authenticate2', token_1: token, token_2: token2 }));
			} else {
				socket.send(JSON.stringify({ type: 'authenticate3', token: token }));
			}
		};

		socket.onmessage = function (event) {
			const data = JSON.parse(event.data);
			switch (data.type) {
				case 'authenticated':
					console.log('Authentication successful');
					break;
				case 'waiting_room':
					console.log('Entered the WAITING ROOM');
					break;
				case 'game_start':
					console.log('Game started:', data.game_id, '(', data.player1, 'vs', data.player2, ')');
					gameContainer.style.display = 'flex';
					document.addEventListener('keydown', handleKeyDown);
					break;
				case 'game_state_update':
					updateGameState(data.game_state);
					break;
				case 'player_disconnected':
					console.log('Player disconnected:', data.player);
					break;
				case 'game_ended':
					console.log('Game ended:', data.game_id);
					break;
				case 'error':
					console.error(data.message);
					break;
				case 'update_tournament_waiting_room':
					document.getElementById('tournament-bracket').innerHTML = data.html;
					const startButton = document.getElementById('start-tournament-btn');
					if (startButton) {
						startButton.addEventListener('click', function() {
							if (typeof socket !== 'undefined' && socket.readyState === WebSocket.OPEN) {
								console.log('Start TOURNAMENT sent..');
								socket.send(JSON.stringify({ type: 'start_tournament' }));
							} else {
								console.error('WebSocket is not open or undefined');
							}
						});
					}
					break;
				case 'update_brackets':
					document.getElementById('tournament-bracket').innerHTML = data.html;
					break;
				case 'tournament_end':
					console.log('Tournament ended, the winner is:', data.winner);
					break;
				case 'tournament_match':
					console.log('Prochain match du tournoi:', data.message);
					if (chatManager.chatSocket && chatManager.chatSocket.readyState === WebSocket.OPEN) {
						chatManager.chatSocket.send(JSON.stringify({
							type: 'chat_message',
							message: data.message,
							username: 'Server',
							room: 'tournament'
						}));
					}
					break;
				default:
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
		console.log("Key pressed:", event.key);
		if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'w' || event.key === 's') {
			sendKeyPress(event.key.toLowerCase());
		}
	}

	function sendKeyPress(key) {
		console.log("Sending key press:", key);
		if (socket.readyState === WebSocket.OPEN) {
			socket.send(JSON.stringify({ type: 'key_press', key }));
		} else {
			console.warn("WebSocket is not open. Key press not sent.");
		}
	}

	function updateGameState(newState) {
        gameState = newState;
        renderGame();
        checkForWinner();
    }

	function renderGame() {
		console.log("Rendering game state...");
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

        logo.style.display = 'block'

        formBlock.style.display = 'block';
        postFormButtons.style.display = 'flex';
    
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
///////////////////////CHECK STATS//////////////////////////////////////
	function sendStatsCommand(targetUser) {
		console.log(`Detected stats command for user: ${targetUser}`);
			fetchPlayers().then((players) => {
			if (!players) {
				console.log('No players found.');
				return;
			}
			const playerStats = filterPlayers(targetUser, players); // Passer le tableau players en paramètre
			if (playerStats) {
				displayPlayerStats(playerStats);
			} else {
				console.log(`Player with username ${targetUser} not found.`);
			}
		}).catch(error => {
			console.error('Error fetching players:', error);
		});
	}

	function filterPlayers(targetUser, players) {
		const searchValue = targetUser.toLowerCase();

		for (let i = 0; i < players.length; i++) {
			const player = players[i];
			if (player.name && player.name.toLowerCase() === searchValue) {
				const playerStats = {
					username: player.name,
					total_matches: player.total_match,
					total_wins: player.total_win,
					win_percentage: player.p_win,
					best_score: player.best_score || 'N/A'
				};
				return playerStats;
			}
		}
		return null;
	}

	function displayPlayerStats(stats) {
		let statsPopup = document.getElementById('player-stats-popup');
		
		if (!statsPopup) {
			statsPopup = document.createElement('div');
			statsPopup.id = 'player-stats-popup';
			statsPopup.classList.add('player-stats-popup');
			document.body.appendChild(statsPopup);
		}
		statsPopup.innerHTML = `
			<h3>Player Stats</h3>
			<p><strong>Username:</strong> ${stats.username}</p>
			<p><strong>Total Matches:</strong> ${stats.total_matches}</p>
			<p><strong>Total Wins:</strong> ${stats.total_wins}</p>
			<p><strong>Win Percentage:</strong> ${stats.win_percentage}%</p>
			<p><strong>Best Score:</strong> ${stats.best_score}</p>
		`;
		statsPopup.classList.add('show');
		statsPopup.classList.remove('hide');
		setTimeout(() => {
			statsPopup.classList.remove('show');
			statsPopup.classList.add('hide');
		}, 5000);
	}

////////////////////////////CHAT////////////////////////////////////
	class ChatManager {
		constructor(username, token) {
			this.username = username;
			this.token = token;
			this.roomSockets = {};
			this.blockedUsers = [];
			this.activeRoom = null;
			this.chatSocket = null;
		}
		startChatWebSocket(roomName) {
			if (!this.username || this.username.trim() === '') {
				alert("Username is required to join the chat. Please log in.");
				return;
			}
			if (this.roomSockets[roomName] && this.roomSockets[roomName].readyState === WebSocket.OPEN) {
				console.warn(`WebSocket for room ${roomName} already open.`);
				return;
			}
			try {
				this.chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat/${roomName}/`);
				this.roomSockets[roomName] = this.chatSocket;
				const chatInputInstance = new ChatInput(roomName, this.username, this.chatSocket, this);
	
				this.chatSocket.onopen = () => {
					this.chatSocket.send(JSON.stringify({
						'type': 'authenticate',
						'username': this.username,
						'token': this.token,
						'room': roomName,
					}));
				};
					
				this.chatSocket.onmessage = (event) => {
					const data = JSON.parse(event.data);
					console.log(`Message received from server in room ${roomName}:`, data);
					const receivedUsername = data.username || this.username;
					let chatLog = document.getElementById(`chat-log-${roomName}`);
					if (!chatLog) {
						console.error(`Chat log element for room ${roomName} not found.`);
						return;
					}
					switch (data.type) {
						case 'authenticated':
							console.log(`User authenticated successfully in room: ${roomName}`);
							break;
	
							case 'chat_message':
								const message = data.message;
								const receivedUsername = data.username;
								const roomName = data.room;
								if (!this.blockedUsers.includes(receivedUsername)) {
									const messageElement = document.createElement('div');
									messageElement.textContent = `${receivedUsername}: ${message}`;
									chatLog.appendChild(messageElement);
									console.log(`Message displayed in chat log for room: ${roomName}`);
								} else {
									console.log(`Message from blocked user ${receivedUsername} was filtered out.`);
								}
								break;
	
						case 'block_user':
							if (data.message) {
								const messageElement = document.createElement('div');
								messageElement.textContent = data.message;
								chatLog.appendChild(messageElement); // Ajoute le message au chat-log
							} else {
								console.error(`Failed to block user: ${data.message}`);
								alert(`Error: Failed to block user. ${data.message}`);
							}
							break;
											
						case 'invite':
							// Vérifie si l'invitation est destinée à cet utilisateur (invité)
							if (data.target_user === this.username) {
								console.log(`Invitation reçue de ${data.inviter}`);
							
								const messageElement = document.createElement('div');
								messageElement.textContent = data.message;
								chatLog.appendChild(messageElement);  // Affiche le message dans le chat-log
							
								// Demande à l'utilisateur s'il accepte ou refuse l'invitation
								const inviteResponse = confirm(`${data.inviter} vous a invité dans la room ${data.room}. Accepter? yes/no.`);
								const response = inviteResponse ? 'yes' : 'no';
							
								console.log(`Réponse à l'invitation: ${response}`);
							
								// Envoie la réponse (oui ou non) au serveur
								this.chatSocket.send(JSON.stringify({
									'type': 'invite_response',
									'username': this.username,  // Utilisateur invité
									'response': response,
									'inviter': data.inviter,  // Le nom de l'invitant
									'room': data.room
								}));
							
								if (response === 'yes') {
									// Si l'invitation est acceptée, lancer QuickMatch pour l'invité
									console.log(`L'invité ${this.username} va démarrer le QuickMatch...`);
									// Si l'invitation est acceptée, lancer QuickMatch pour l'invité après un délai
									console.log("Invitation acceptée, démarrage du QuickMatch pour l'invité après un délai...");
									setTimeout(() => {
										console.log("Appel de startQuickMatch(invite)...");
										startQuickMatch();  // Lancer le jeu après 2 secondes
										console.log("startQuickMatch appelé.");
									}, 2000);  // 2000 millisecondes = 2 secondes
								}
							}
							break;
																								
						case 'invite_response':
    						// Vérifie si l'invitation concerne cet utilisateur (l'invitant)
   							if (data.inviter === this.username) {
        						const messageElement = document.createElement('div');
        						messageElement.textContent = data.message;
        						chatLog.appendChild(messageElement);  // Affiche la réponse dans le chat-log
        						console.log(`Réponse à l'invitation: ${data.message}`);

							if (data.response && data.response.toLowerCase() === 'yes') {
								console.log("Invitation acceptée, démarrage du QuickMatch pour l'invitant...");
								console.log("Appel de startQuickMatch...(invite response)");
								startQuickMatch();
								console.log("startQuickMatch appelé.");
							}
    					}
    					break;

						case 'player_stats':
							console.log('Player stats received:', data);
							displayPlayerStats(data.stats);
							break;

						case 'error':
							console.error('Error message received:', data.message);
							alert('Error: ' + data.message);
							break;
	
						default:
							console.warn('Unhandled message type:', data);
					}
				};
	
				// Gestion de la fermeture du WebSocket
				this.chatSocket.onclose = (event) => {
					if (event.wasClean) {
						console.log(`Chat WebSocket closed cleanly for room ${roomName}, code=${event.code}, reason=${event.reason}`);
					} else {
						console.error(`Chat WebSocket closed unexpectedly for room ${roomName}`);
					}
				};
	
				// Gestion des erreurs WebSocket
				this.chatSocket.onerror = (error) => {
					console.error(`Chat WebSocket error in room ${roomName}:`, error);
				};
	
			} catch (error) {
				console.error(`Error initializing chat WebSocket for room ${roomName}:`, error);
			}
		}
	
		blockUser(targetUser) {
			this.blockedUsers.push(targetUser);
			console.log(`User ${targetUser} added to blocked list.`);
		}

		createRoomTab(roomName) {
			console.log(`createRoomTab: ${roomName} with username: ${username} and token: ${token}`);
	
			const tabContainer = document.getElementById('room-tabs-container');
			if (!tabContainer) {
				console.error('Room tabs container not found.');
				return;
			}
	
			const existingTab = Array.from(tabContainer.children).find(tab => tab.dataset.room === roomName);
			if (existingTab) {
				console.log(`Tab for room ${roomName} already exists.`);
				// Vous pouvez ajouter une classe pour indiquer que l'onglet est inactif
				existingTab.classList.remove('active');
			} else {
				console.warn(`Tab for room ${roomName} not found in the HTML.`);
			}
		}
		
		showRoomTab(roomName) {
			const tabContainer = document.getElementById('room-tabs-container');
			const tab = Array.from(tabContainer.children).find(tab => tab.dataset.room === roomName);
			if (tab) {
				tab.classList.add('active');
				console.log(`Showing tab for room: ${roomName}`);
			} else {
				console.warn(`Tab for room ${roomName} not found.`);
			}
		}
		
		switchRoom(roomName) {
			
			if (!roomName) {
				console.error('Room name is undefined.');
				return;
			}
			console.log(`Attempting to switch to room: ${roomName}`);
			if (activeRoom === roomName) {
				console.log(`Already in room: ${roomName}`);
				return;
			}
	
			console.log(`Switching from room ${activeRoom} to room ${roomName}`);
			const previousRoom = activeRoom;
			activeRoom = roomName;
	
			if (previousRoom && document.getElementById(`chat-log-${previousRoom}`)) {
				console.log(`Hiding chat log for previous room: ${previousRoom}`);
				document.getElementById(`chat-log-${previousRoom}`).style.display = 'none';
			}
	
			const chatLog = document.getElementById(`chat-log-${roomName}`);
			if (chatLog) {
				chatLog.style.display = 'block';
			} else {
				console.warn(`No chat log found for room: ${roomName}`);
			}
		
			// Mettre à jour l'affichage des inputs
			document.querySelectorAll('.chat-input').forEach(input => {
				input.style.display = 'none';
			});
			document.getElementById(`chat-input-${roomName}`).style.display = 'block';
	
			// Mettre à jour l'onglet actif
			const tabs = document.querySelectorAll('.room-tab');
			tabs.forEach(t => t.classList.remove('active'));
			const activeTab = Array.from(tabs).find(tab => tab.dataset.room === roomName);
			if (activeTab) {
				activeTab.classList.add('active');
			}
		}
		
		joinRoom(roomName) {
			console.log(`Joining room: ${roomName} with username: ${chatManager.username} and token: ${chatManager.token}`);
			if (activeRoom === roomName) {
				console.log(`Already in room: ${roomName}`);
				return;
			}
		
			// Si la room n'a pas de WebSocket actif, on le crée
			if (!chatManager.roomSockets[roomName]) {
				console.log(`Joining new room: ${roomName}`);
				this.createRoomTab(roomName);
				this.showRoomTab(roomName);
				this.startChatWebSocket(roomName); //ChatManager pour démarrer le WebSocket
			}
		
			this.switchRoom(roomName);
			// Activer l'affichage du conteneur de chat
    		document.getElementById('chat-container').style.display = 'flex';
		}

		leaveRoom(roomName) {
			if (this.roomSockets[roomName]) {
				console.log(`Leaving room: ${roomName}`);
				this.roomSockets[roomName].close();
				delete this.roomSockets[roomName];
				if (this.activeRoom === roomName) {
					this.activeRoom = null;
					this.chatSocket = null;
				}
			} else {
				console.warn(`No active WebSocket found for room: ${roomName}`);
			}
		}
}

	class ChatInput {
		constructor(roomName, username, chatSocket, chatManager) {
			this.roomName = roomName;
			this.username = username;
			this.chatSocket = chatSocket;
			this.chatManager = chatManager;
			this.messageInput = document.querySelector(`#chat-input-${roomName} input`);
			this.chatButton = document.querySelector(`#chat-input-${roomName} button`);
	
			console.log(`ChatInput initialized for room: ${roomName}, username: ${username}`);
			this.initEventListeners();
		}
	
		initEventListeners() {
			this.messageInput.addEventListener('keypress', (event) => {
				if (event.key === 'Enter') {
					console.log("Enter key pressed, attempting to send message...");
					this.sendMessage();
				}
			});
	
			this.chatButton.addEventListener('click', () => {
				console.log("Send button clicked, attempting to send message...");
				this.sendMessage();
			});
		}
	
		sendMessage() {
			const message = this.messageInput.value.trim();
			console.log(`Attempting to send message: ${message}`);
	
			if (message) {
				if (message.startsWith('/b ')) {
					const targetUser = message.slice(3).trim();
					console.log(`Detected block command for user: ${targetUser}`);
					this.sendBlockCommand(targetUser);
				} else if (message.startsWith('/i ')) {
					const targetUser = message.slice(3).trim();
					console.log(`Detected invite command for user: ${targetUser}`);
					this.sendInviteCommand(targetUser);
				} else if (message.startsWith('/s ')) {
					const targetUser = message.slice(3).trim();
					console.log(`Detected stats command for user: ${targetUser}`);
					sendStatsCommand(targetUser);
				} else {
					console.log(`Sending chat message to WebSocket...`);
					this.chatSocket.send(JSON.stringify({
						'type': 'chat_message',
						'username': this.username,
						'message': message,
						'room': this.roomName
					}));
				}
				this.messageInput.value = '';
				console.log("Message input cleared.");
			} else {
				console.warn('Cannot send an empty message.');
			}
		}
	
		sendBlockCommand(targetUser) {
			this.chatManager.blockUser(targetUser); // Met à jour la liste des utilisateurs bloqués via ChatManager
			console.log(`Sending block command to WebSocket for user: ${targetUser}`);
			this.chatSocket.send(JSON.stringify({
				'type': 'block_user',
				'username': this.username,
				'target_user': targetUser,
				'room': this.roomName
			}));
		}
	
		sendInviteCommand(targetUser) {
			if (!targetUser) {
				console.error("Target user is not defined. Cannot send invite.");
				return;
			}
			if (!this.username) {
				console.error("Username is not defined. Cannot send invite.");
				return;
			}
			if (!this.roomName) {
				console.error("Room name is not defined. Cannot send invite.");
				return;
			}
		
			console.log(`Sending invite command to WebSocket for user: ${targetUser}`);
		
			this.chatSocket.send(JSON.stringify({
				'type': 'invite',
				'username': this.username,  // Utilisateur qui envoie l'invitation
				'target_user': targetUser,   // Utilisateur qui reçoit l'invitation
				'room': this.roomName        // Room où l'invitation est faite
			}));
			}
		}
	});