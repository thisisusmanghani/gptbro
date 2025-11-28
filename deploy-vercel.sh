#!/bin/bash

# Vercel Deployment Script for ChatBot
# Run this script to deploy to Vercel production

echo "🚀 Starting Vercel Deployment..."
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null
then
    echo "❌ Vercel CLI not found!"
    echo "📦 Installing Vercel CLI..."
    npm i -g vercel
fi

echo "✅ Vercel CLI found"
echo ""

# Check environment variables
echo "🔍 Checking environment variables..."
if vercel env ls | grep -q "GEMINI_API_KEY"; then
    echo "✅ GEMINI_API_KEY is set in Vercel"
else
    echo "⚠️  WARNING: GEMINI_API_KEY not found in Vercel!"
    echo "📝 Please set it in Vercel Dashboard:"
    echo "   https://vercel.com/dashboard → Settings → Environment Variables"
    echo ""
    read -p "❓ Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        echo "❌ Deployment cancelled"
        exit 1
    fi
fi

echo ""
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo ""
echo "🚀 Deploying to Vercel Production..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Check deployment URL in terminal output"
echo "   2. Visit the URL to test your app"
echo "   3. Check Vercel Dashboard → Functions → Logs if issues occur"
echo ""
echo "🎉 Done! Your app is live!"
