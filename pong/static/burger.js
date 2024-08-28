document.addEventListener('DOMContentLoaded', () => {

    const menuButton = document.querySelector('.burger-menu');
    const dropdownMenu = document.getElementById('dropdown-menu');

    const playerList = document.getElementById('player-list');
    const matchList = document.getElementById('match-list');
    const tournoiList = document.getElementById('tournoi-list');
    const blockchainList = document.getElementById('blockchain-list');

    menuButton.addEventListener('click', toggleMenu);

        function toggleMenu() {
            console.log('Menu toggled');
            if (dropdownMenu.style.display === "block") {
                dropdownMenu.style.display = "none";
                hideAllTables();
            } else {
                dropdownMenu.style.display = "block";
            }
        }

        function hideAllTables(){
            if (playerList) playerList.style.display = 'none';
            if (matchList) matchList.style.display = 'none';
            if (tournoiList) tournoiList.style.display = 'none';
            if (blockchainList) blockchainList.style.display = 'none';
        }

        const links = document.querySelectorAll('#dropdown-menu a');

        links.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const tableId = link.getAttribute('data-table');
                showTable(tableId);
            });
        });
        
        function showTable(tableId) {
            hideAllTables();
        
            
            if (tableId === 'player-list') {
                playerList.style.display = 'block';
                fetchPlayers();
            } else if (tableId === 'match-list') {
                matchList.style.display = 'block';
                fetchMatches();
            } else if (tableId === 'tournoi-list') { 
                tournoiList.style.display = 'block';
                fetchTournois();
            } else if (tableId === 'blockchain-list') {
                console.log('Opening external page in a new tab');
                window.open('https://sepolia.etherscan.io/address/0x078d04eb6fb97cd863361fc86000647dc876441b', '_blank');
            }

            if (dropdownMenu) {
                dropdownMenu.style.display = 'none';
            }
        }

        function fetchMatches() {
            console.log('Fetching matches...');
            fetch('/api/match_list/')
                .then(response => response.json())
                .then(data => {
                    if (data.matches) {
                        displayMatches(data.matches);
                    }
                })
                .catch(error => console.error('Error fetching match data:', error));
        }

        function fetchPlayers(){
            console.log('Fetching players...');
            fetch('/api/player_list/')
                .then(response => response.json())
                .then(data => {
                    if (data.players) {
                        displayPlayers(data.players);
                    }
                })
                .catch(error => console.error('Error fetching match data:', error));
        }

        function fetchTournois(){
            console.log('Fetching tournois...');
            fetch('/api/tournoi_list/')
                .then(response => response.json())
                .then(data => {
                    if (data.tournois) {
                        displayTournois(data.tournois);
                    }
                })
                .catch(error => console.error('Error fetching match data:', error));
        }

        function displayMatches(matches) {
            console.log('Displaying matches:');
            const matchListBody = document.querySelector('#match-list tbody');
            matchListBody.innerHTML = '';

            if (matches.length != 0) {
                matches.forEach(match => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${match.id}</td>
                        <td>${match.player1__name}</td>
                        <td>${match.player2__name}</td>
                        <td>${match.score_player1}</td>
                        <td>${match.score_player2}</td>
                        <td>${match.winner__name}</td>
                        <td>${match.nbr_ball_touch_p1}</td>
                        <td>${match.nbr_ball_touch_p2}</td>
                        <td>${match.duration}</td>
                        <td>${match.date}</td>
                        <td>${match.is_tournoi}</td>
                        <td>${match.tournoi__name}</td>
                        `;
                    matchListBody.appendChild(row);
                });
            } else {
                row.innerHTML = `
                    <td colspan="12">No matches found.</td>
                `;
                matchListBody.appendChild(row);
            }
        }

        function displayPlayers(players) {
            console.log('Displaying players:');
            const playersListBody = document.querySelector('#player-list tbody');
            playersListBody.innerHTML = '';

            if (players.length != 0) {
                players.forEach(player => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${player.id}</td>
                        <td>${player.name}</td>
                        <td>${player.total_match}</td>
                        <td>${player.total_win}</td>
                        <td>${player.p_win}</td>
                        <td>${player.m_score_match}</td>
                        <td>${player.m_score_adv_match}</td>
                        <td>${player.best_score}</td>
                        <td>${player.m_nbr_ball_touch}</td>
                        <td>${player.total_duration}</td>
                        <td>${player.m_duration}</td>
                        <td>${player.num_participated_tournaments}</td>
                        <td>${player.num_won_tournaments}</td>
                        `;
                    playersListBody.appendChild(row);
                });
            } else {
                row.innerHTML = `
                    <td colspan="12">No matches found.</td>
                    `
                playersListBody.appendChild(row);
            }
        }

        function displayTournois(tournois) {
            console.log('Displaying tournois:');
            const tournoisListBody = document.querySelector('#tournoi-list tbody');
            tournoisListBody.innerHTML = '';

            if (tournois.length != 0) {
                tournois.forEach(tournoi => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${tournoi.id}</td>
                        <td>${tournoi.name}</td>
                        <td>${tournoi.nbr_player}</td>
                        <td>${tournoi.date}</td>
                        <td>${tournoi.winner.name}</td>
                        `;
                    tournoisListBody.appendChild(row);
                });
            } else {
                row.innerHTML = `
                    <td colspan="12">No matches found.</td>
                    `
                tournoisListBody.appendChild(row);
            }
    
        }

        document.getElementById('search-player').addEventListener('input', filterPlayers);
        document.getElementById('search-match-player').addEventListener('input', filterMatches);
        document.getElementById('search-match-date').addEventListener('input', filterMatches);

        function filterPlayers() {
            const searchValue = document.getElementById('search-player').value.toLowerCase();
            const playersListBody = document.querySelector('#player-list tbody');
            const rows = playersListBody.getElementsByTagName('tr');

            for (let i = 0; i < rows.length; i++) {
                const nameCell = rows[i].getElementsByTagName('td')[1];
                if (nameCell) {
                    const nameValue = nameCell.textContent || nameCell.innerText;
                    if (nameValue.toLowerCase().indexof(searchValue) > -1 ) {
                        rows[i].style.display = '';
                    } else {
                        rows[i].style.display = 'none';
                    }
                }
            }
        }

        function filterMatches() {
            const playerSearchValue = document.getElementById('search-match-player').value.toLowerCase();
            const dateSearchValue = document.getElementById('search-match-date').value;
            const matchListBody = document.querySelector('#match-list tbody');
            const rows = matchListBody.getElementsByTagName('tr');

            for (let i = 0; i < rows.length; i++) {
                const player1Cell = rows[i].getElementsByTagName('td')[1]; 
                const player2Cell = rows[i].getElementsByTagName('td')[2]; 
                const dateCell = rows[i].getElementsByTagName('td')[9]; 
                
                let playerMatch = true;
                if (playerSearchValue) {
                    const player1Value = player1Cell.textContent || player1Cell.innerText;
                    const player2Value = player2Cell.textContent || player2Cell.innerText;
                    playerMatch = player1Value.toLowerCase().indexOf(playerSearchValue) > -1 ||
                                player2Value.toLowerCase().indexOf(playerSearchValue) > -1;
                }

                let dateMatch = true;
                if (dateSearchValue) {
                    const dateValue = dateCell.textContent || dateCell.innerText;
                    dateMatch = dateValue.startsWith(dateSearchValue);
                }

                if (playerMatch && dateMatch) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        }
});