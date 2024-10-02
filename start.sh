# Step 1: Check if the frontend directory exists
if [ ! -d "frontend" ]; then
    echo "Frontend directory not found"
    exit 1
fi

# Step 2: Navigate to the frontend folder and install npm dependencies
echo "Installing npm dependencies in the frontend directory..."
cd frontend || { echo "Failed to change directory to frontend"; exit 1; }
npm install

# Step 3: Run both frontend and backend using concurrently
echo "Starting both frontend and backend..."
npx concurrently "npm run start-frontend" "npm run start-backend"