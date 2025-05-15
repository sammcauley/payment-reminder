provider "google" {
    project = var.project_id
    region = "europe-west2"
}

resource "google_project_service" "sheets_api" {
    project = var.project_id
    service = "sheets.googleapis.com"
}

resource "google_service_account" "sheets_service_account" {
    account_id = "sheets-access"
    display_name = "Sheets Access"
}

resource "google_service_account_key" "sheets_key" {
    service_account_id = google_service_account.sheets_service_account.name
    private_key_type = "TYPE_GOOGLE_CREDENTIALS_FILE"
}