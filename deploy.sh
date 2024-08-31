# deploy.sh

# Load the .env file into environment variables
export $(cat .env | xargs)

# Build the Docker image
sudo docker buildx build --platform linux/amd64 -t data-analyst .

# Tag and push the Docker image to GCR
docker tag data-analyst gcr.io/$GCP_PROJECT_ID/data-analyst:latest
docker push gcr.io/$GCP_PROJECT_ID/data-analyst:latest

# Deploy to Google Cloud Run
gcloud run deploy data-analyst-service \
  --image gcr.io/$GCP_PROJECT_ID/data-analyst:latest \
  --platform managed \
  --region europe-north1 \
  --allow-unauthenticated \
  --set-env-vars "OPENAI_API_KEY=$OPENAI_API_KEY,GROQ_API_KEY=$GROQ_API_KEY"