@echo off
REM Vercel Deployment Script for ChatBot (Windows)
REM Run this script to deploy to Vercel production

echo.
echo 🚀 Starting Vercel Deployment...
echo.

REM Check if vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Vercel CLI not found!
    echo 📦 Installing Vercel CLI...
    call npm i -g vercel
)

echo ✅ Vercel CLI found
echo.

REM Check environment variables
echo 🔍 Checking environment variables...
vercel env ls | findstr /C:"GEMINI_API_KEY" >nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  WARNING: GEMINI_API_KEY not found in Vercel!
    echo 📝 Please set it in Vercel Dashboard:
    echo    https://vercel.com/dashboard → Settings → Environment Variables
    echo.
    set /p CONTINUE="❓ Do you want to continue anyway? (y/N): "
    if /i not "%CONTINUE%"=="y" (
        echo ❌ Deployment cancelled
        exit /b 1
    )
) else (
    echo ✅ GEMINI_API_KEY is set in Vercel
)

echo.
echo 📦 Building frontend...
cd frontend
call npm install
call npm run build
cd ..

echo.
echo 🚀 Deploying to Vercel Production...
call vercel --prod

echo.
echo ✅ Deployment complete!
echo.
echo 📋 Next steps:
echo    1. Check deployment URL in terminal output
echo    2. Visit the URL to test your app
echo    3. Check Vercel Dashboard → Functions → Logs if issues occur
echo.
echo 🎉 Done! Your app is live!
pause
