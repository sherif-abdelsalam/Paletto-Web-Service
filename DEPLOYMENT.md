# Flask Image Color Palette API - Render Deployment Guide

## Prerequisites

- Git repository (GitHub/GitLab)
- Render account
- Cloud storage for the large model file (Google Drive, Dropbox, AWS S3, etc.)

## Step 1: Upload Your Model File to Cloud Storage

Since your `ImageRecoloring.h5` file is 506MB (too large for Git), you need to:

1. Upload `ImageRecoloring.h5` to a cloud storage service:

   - **Google Drive**: Upload and get a direct download link
   - **Dropbox**: Upload and create a direct download link
   - **AWS S3**: Upload and create a public URL
   - **Any file hosting service that provides direct download URLs**

2. Get the direct download URL for the model file

## Step 2: Configure Environment Variable

In your Render dashboard, add an environment variable:

- **Key**: `MODEL_URL`
- **Value**: Your model file's direct download URL

## Step 3: Deploy to Render

1. **Connect Repository**:

   - Go to render.com → New → Web Service
   - Connect your GitHub/GitLab repository

2. **Service Configuration**:

   - **Name**: `image-color-palette-api`
   - **Region**: Choose your preferred region
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Environment Variables**:

   - Add `MODEL_URL` with your model file's download URL

4. **Deploy**: Click "Create Web Service"

## Step 4: Test Your Deployment

Once deployed, your API will be available at:
`https://your-service-name.onrender.com`

Test the endpoint:

```bash
curl -X POST https://your-service-name.onrender.com/process_image \
  -H "Content-Type: image/jpeg" \
  --data-binary @your-test-image.jpg
```

## Important Notes

- First deployment may take 10-15 minutes due to model download
- Render free tier has usage limits
- The service may sleep after 15 minutes of inactivity (free tier)
- Model file is downloaded once and cached during the build process

## Troubleshooting

- Check Render logs for any deployment issues
- Ensure MODEL_URL is a direct download link
- Verify all dependencies are in requirements.txt
