

# Navigate to the Frontend folder and install npm dependencies
echo "Installing npm dependencies in the Frontend directory..."
cd Frontend || { echo "Frontend directory not found"; exit 1; }
npm install

# Go back to the project root to run both frontend and backend using concurrently
cd .. || { echo "Failed to return to project root"; exit 1; }

# Run both frontend and backend using concurrently
echo "Starting both frontend and backend..."
npx concurrently "npm run dev" "python ./backend/src/main.py"
