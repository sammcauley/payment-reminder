# Payment Reminder

## Project setup instructions
### 1. Prerequisites
 - Install Terraform
 - Install Git
 - Install gcloud CLI

 ### 2. Clone the repository
 ```bash
 git clone https://github.com/sammcauley/payment-reminder.git
 cd payment-reminder
 ```

 ### 3. Setup Google Cloud Project
 1. Create a new Google Cloud project via the console
 2. Enable billing

 ### 4. Inital authentication
 `gcloud auth application-default login`

 ### 5. Run Terraform to create resources
 ```bash
 cd terraform
 terraform init
 terraform apply
 ```

 ### 6. Save and set service account credentials
`source save-key-set-env.sh`
<br>Optionally you can add the env variable in your .bashrc