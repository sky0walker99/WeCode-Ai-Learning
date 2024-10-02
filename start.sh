# Navigate to the Frontend folder and install npm dependencies
echo "Installing npm dependencies in the Frontend directory..."
cd Frontend || { echo "Frontend directory not found"; exit 1; }
npm install

# Start the frontend
npm run dev &

# Go back to the root directory
cd ..

# Start the backend
echo "Starting the backend..."
python ./backend/src/main.py
