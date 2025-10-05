# Test number assignment and SMS sending
$baseUrl = "http://localhost:8082"

# Login to get token
$loginBody = @{
    username = "admin"
    password = "telecom2025"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.token

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# Get available numbers
$availableNumbers = Invoke-RestMethod -Uri "$baseUrl/api/numbers/available" -Method GET -Headers $headers
$firstNumber = $availableNumbers.numbers[0].number
Write-Host "Available number: $firstNumber"

# Assign the number
$assignBody = @{
    number = $firstNumber
} | ConvertTo-Json

$assignResponse = Invoke-RestMethod -Uri "$baseUrl/api/numbers/assign" -Method POST -Body $assignBody -Headers $headers
Write-Host "Assigned number: $($assignResponse.number.number)"

# Use the number to send SMS
$smsBody = @{
    from_ = $firstNumber
    to = "+1234567890"
    message = "Test SMS from assigned number"
} | ConvertTo-Json

$smsResponse = Invoke-RestMethod -Uri "$baseUrl/api/sms/send" -Method POST -Body $smsBody -Headers $headers
Write-Host "SMS sent successfully: $($smsResponse.success)"