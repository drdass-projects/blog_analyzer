#!/bin/bash

echo "🔁 Starting Blog Analyzer Backend and Frontend using PM2..."

# Start backend
echo "➡️  Activating Python virtual environment and starting backend..."
cd ~/blog_analyzer/backend
source venv/bin/activate
pm2 delete blog-backend >/dev/null 2>&1
pm2 start uvicorn --name blog-backend -- main:app --host 0.0.0.0 --port 8000

# Start frontend
echo "➡️  Starting frontend React app..."
cd ~/blog_analyzer/frontend
pm2 delete blog-frontend >/dev/null 2>&1
pm2 start npm --name blog-frontend -- start

# Save PM2 state to auto-start on reboot
echo "💾 Saving PM2 state..."
pm2 save

echo "✅ All services started with PM2"
pm2 status
