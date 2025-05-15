output "sheets_service_account_email" {
    value = google_service_account.sheets_service_account.email
}

output "sheets_key_json" {
    sensitive = true
    value = google_service_account_key.sheets_key.private_key
}