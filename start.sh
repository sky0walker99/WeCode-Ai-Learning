
# Step 1: Navigate to the frontend folder and install npm dependencies
echo "Installing npm dependencies in the frontend directory..."
cd frontend || { echo "Frontend directory not found"; exit 1; }
npm install

# Step 2: Run the development server for both frontend and backend
echo "Starting both frontend and backend..."
npm run dev