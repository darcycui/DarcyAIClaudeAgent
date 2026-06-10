// Game variables
const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const highScoreElement = document.getElementById('high-score');
const finalScoreElement = document.getElementById('final-score');
const speedSlider = document.getElementById('speed-slider');
const speedValueElement = document.getElementById('speed-value');
const gameOverScreen = document.getElementById('game-over');
const welcomeScreen = document.getElementById('welcome');

// Game state
let game = {
    running: false,
    paused: false,
    gameOver: false,
    score: 0,
    highScore: localStorage.getItem('snakeHighScore') || 0,
    speed: 10,
    gridSize: 20,
    gridWidth: canvas.width / 20,
    gridHeight: canvas.height / 20
};

// Snake variables
let snake = {
    body: [],
    direction: { x: 1, y: 0 },
    nextDirection: { x: 1, y: 0 },
    color: '#2ecc71',
    headColor: '#27ae60'
};

// Food variables
let food = {
    x: 0,
    y: 0,
    color: '#e74c3c'
};

// Initialize game
function init() {
    // Set high score
    highScoreElement.textContent = game.highScore;
    speedValueElement.textContent = game.speed;
    
    // Initialize snake
    snake.body = [
        { x: 10, y: 10 },
        { x: 9, y: 10 },
        { x: 8, y: 10 }
    ];
    snake.direction = { x: 1, y: 0 };
    snake.nextDirection = { x: 1, y: 0 };
    
    // Generate first food
    generateFood();
    
    // Draw initial state
    draw();
    
    // Show welcome screen
    welcomeScreen.style.display = 'flex';
    gameOverScreen.style.display = 'none';
}

// Generate food at random position
function generateFood() {
    let validPosition = false;
    
    while (!validPosition) {
        food.x = Math.floor(Math.random() * game.gridWidth);
        food.y = Math.floor(Math.random() * game.gridHeight);
        
        // Check if food is not on snake
        validPosition = true;
        for (let segment of snake.body) {
            if (segment.x === food.x && segment.y === food.y) {
                validPosition = false;
                break;
            }
        }
    }
}

// Draw game elements
function draw() {
    // Clear canvas
    ctx.fillStyle = '#0f1525';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid (optional, for visual reference)
    drawGrid();
    
    // Draw snake
    for (let i = 0; i < snake.body.length; i++) {
        const segment = snake.body[i];
        
        // Set color (head is different)
        if (i === 0) {
            ctx.fillStyle = snake.headColor;
        } else {
            ctx.fillStyle = snake.color;
        }
        
        // Draw snake segment with rounded corners
        drawRoundedRect(
            segment.x * game.gridSize,
            segment.y * game.gridSize,
            game.gridSize,
            game.gridSize,
            4
        );
        
        // Draw eyes on head
        if (i === 0) {
            ctx.fillStyle = '#fff';
            const eyeSize = game.gridSize / 5;
            
            // Calculate eye positions based on direction
            let eyeOffsetX = 0, eyeOffsetY = 0;
            if (snake.direction.x === 1) { // Right
                eyeOffsetX = game.gridSize - eyeSize * 2;
                eyeOffsetY = eyeSize * 1.5;
            } else if (snake.direction.x === -1) { // Left
                eyeOffsetX = eyeSize;
                eyeOffsetY = eyeSize * 1.5;
            } else if (snake.direction.y === 1) { // Down
                eyeOffsetX = eyeSize * 1.5;
                eyeOffsetY = game.gridSize - eyeSize * 2;
            } else if (snake.direction.y === -1) { // Up
                eyeOffsetX = eyeSize * 1.5;
                eyeOffsetY = eyeSize;
            }
            
            ctx.beginPath();
            ctx.arc(
                segment.x * game.gridSize + eyeOffsetX,
                segment.y * game.gridSize + eyeOffsetY,
                eyeSize,
                0,
                Math.PI * 2
            );
            ctx.fill();
            
            ctx.beginPath();
            ctx.arc(
                segment.x * game.gridSize + eyeOffsetX + (snake.direction.x !== 0 ? 0 : game.gridSize - eyeSize * 3),
                segment.y * game.gridSize + eyeOffsetY,
                eyeSize,
                0,
                Math.PI * 2
            );
            ctx.fill();
        }
    }
    
    // Draw food
    ctx.fillStyle = food.color;
    ctx.beginPath();
    ctx.arc(
        food.x * game.gridSize + game.gridSize / 2,
        food.y * game.gridSize + game.gridSize / 2,
        game.gridSize / 2 - 2,
        0,
        Math.PI * 2
    );
    ctx.fill();
    
    // Draw food shine effect
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(
        food.x * game.gridSize + game.gridSize / 3,
        food.y * game.gridSize + game.gridSize / 3,
        game.gridSize / 6,
        0,
        Math.PI * 2
    );
    ctx.fill();
}

// Draw grid lines
function drawGrid() {
    ctx.strokeStyle = 'rgba(52, 152, 219, 0.1)';
    ctx.lineWidth = 1;
    
    // Vertical lines
    for (let x = 0; x <= canvas.width; x += game.gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    
    // Horizontal lines
    for (let y = 0; y <= canvas.height; y += game.gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

// Draw rounded rectangle
function drawRoundedRect(x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
    ctx.fill();
}

// Update game state
function update() {
    if (!game.running || game.paused || game.gameOver) return;
    
    // Update snake direction
    snake.direction = { ...snake.nextDirection };
    
    // Calculate new head position
    const head = { ...snake.body[0] };
    head.x += snake.direction.x;
    head.y += snake.direction.y;
    
    // Check wall collision
    if (
        head.x < 0 || 
        head.x >= game.gridWidth || 
        head.y < 0 || 
        head.y >= game.gridHeight
    ) {
        gameOver();
        return;
    }
    
    // Check self collision
    for (let segment of snake.body) {
        if (segment.x === head.x && segment.y === head.y) {
            gameOver();
            return;
        }
    }
    
    // Add new head
    snake.body.unshift(head);
    
    // Check food collision
    if (head.x === food.x && head.y === food.y) {
        // Increase score
        game.score += 10;
        scoreElement.textContent = game.score;
        
        // Update high score if needed
        if (game.score > game.highScore) {
            game.highScore = game.score;
            highScoreElement.textContent = game.highScore;
            localStorage.setItem('snakeHighScore', game.highScore);
        }
        
        // Generate new food
        generateFood();
        
        // Increase speed slightly every 5 foods
        if (game.score % 50 === 0 && game.speed < 20) {
            game.speed++;
            speedSlider.value = game.speed;
            speedValueElement.textContent = game.speed;
        }
    } else {
        // Remove tail if no food eaten
        snake.body.pop();
    }
    
    // Draw updated game
    draw();
}

// Game over function
function gameOver() {
    game.running = false;
    game.gameOver = true;
    
    // Update final score
    finalScoreElement.textContent = game.score;
    
    // Show game over screen
    gameOverScreen.style.display = 'flex';
    
    // Update button states
    document.getElementById('start-btn').disabled = false;
    document.getElementById('pause-btn').disabled = true;
    document.getElementById('pause-btn').innerHTML = '<i class="fas fa-pause"></i> Pause';
}

// Start game
function startGame() {
    if (game.running && !game.paused) return;
    
    game.running = true;
    game.paused = false;
    game.gameOver = false;
    
    // Reset score if starting new game
    if (!game.paused) {
        game.score = 0;
        scoreElement.textContent = '0';
        init();
    }
    
    // Hide screens
    welcomeScreen.style.display = 'none';
    gameOverScreen.style.display = 'none';
    
    // Update button states
    document.getElementById('start-btn').disabled = true;
    document.getElementById('pause-btn').disabled = false;
}

// Pause/resume game
function togglePause() {
    if (!game.running || game.gameOver) return;
    
    game.paused = !game.paused;
    
    const pauseBtn = document.getElementById('pause-btn');
    if (game.paused) {
        pauseBtn.innerHTML = '<i class="fas fa-play"></i> Resume';
    } else {
        pauseBtn.innerHTML = '<i class="fas fa-pause"></i> Pause';
    }
}

// Reset game
function resetGame() {
    game.running = false;
    game.paused = false;
    game.gameOver = false;
    game.score = 0;
    game.speed = parseInt(speedSlider.value);
    
    scoreElement.textContent = '0';
    speedValueElement.textContent = game.speed;
    
    document.getElementById('start-btn').disabled = false;
    document.getElementById('pause-btn').disabled = true;
    document.getElementById('pause-btn').innerHTML = '<i class="fas fa-pause"></i> Pause';
    
    init();
}

// Handle keyboard input
function handleKeyDown(e) {
    switch (e.key) {
        case 'ArrowUp':
        case 'w':
        case 'W':
            if (snake.direction.y === 0) {
                snake.nextDirection = { x: 0, y: -1 };
            }
            break;
            
        case 'ArrowDown':
        case 's':
        case 'S':
            if (snake.direction.y === 0) {
                snake.nextDirection = { x: 0, y: 1 };
            }
            break;
            
        case 'ArrowLeft':
        case 'a':
        case 'A':
            if (snake.direction.x === 0) {
                snake.nextDirection = { x: -1, y: 0 };
            }
            break;
            
        case 'ArrowRight':
        case 'd':
        case 'D':
            if (snake.direction.x === 0) {
                snake.nextDirection = { x: 1, y: 0 };
            }
            break;
            
        case ' ':
        case 'Spacebar':
            if (game.gameOver) {
                resetGame();
                startGame();
            } else if (!game.running) {
                startGame();
            } else {
                resetGame();
            }
            e.preventDefault();
            break;
            
        case 'p':
        case 'P':
            if (game.running) {
                togglePause();
            }
            break;
    }
}

// Event listeners
document.getElementById('start-btn').addEventListener('click', startGame);
document.getElementById('pause-btn').addEventListener('click', togglePause);
document.getElementById('reset-btn').addEventListener('click', resetGame);
document.getElementById('restart-btn').addEventListener('click', () => {
    resetGame();
    startGame();
});

speedSlider.addEventListener('input', () => {
    game.speed = parseInt(speedSlider.value);
    speedValueElement.textContent = game.speed;
});

document.addEventListener('keydown', handleKeyDown);

// Game loop
function gameLoop() {
    update();
    
    // Calculate frame delay based on speed
    const delay = Math.max(50, 200 - (game.speed * 10));
    
    setTimeout(gameLoop, delay);
}

// Initialize and start game loop
init();
gameLoop();