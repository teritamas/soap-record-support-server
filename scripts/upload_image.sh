REGION=asia-northeast1
PROJECT_ID=hackday-327101

gcloud config set project ${PROJECT_ID}
gcloud config set run/region ${REGION}

gcloud builds submit --tag gcr.io/${PROJECT_ID}/soap-record-support-server:latest

gcloud run deploy soap-record-support-server --image gcr.io/${PROJECT_ID}/soap-record-support-server:latest