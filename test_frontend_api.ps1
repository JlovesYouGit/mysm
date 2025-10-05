# Test frontend API connectivity
$baseUrl = "http://localhost:8084"

Write-Host "Testing API connectivity..."

# Test 1: Health check
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
    Write-Host "✅ Health check: $($health.status)"
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)"
}

# Test 2: Login
try {
    $loginBody = @{
        username = "admin"
        password = "telecom2025"
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
    $token = $loginResponse.token
    Write-Host "✅ Login successful"
    
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }

    # Test 3: Available numbers
    try {
        $availableNumbers = Invoke-RestMethod -Uri "$baseUrl/api/numbers/available" -Method GET -Headers $headers
        Write-Host "✅ Available numbers: $($availableNumbers.numbers.Count) found"
        
        if ($availableNumbers.numbers.Count -gt 0) {
            $firstNumber = $availableNumbers.numbers[0].number
            Write-Host "First available number: $firstNumber"
            
            # Test 4: Assign number
            try {
                $assignBody = @{
                    number = $firstNumber
                } | ConvertTo-Json

                $assignResponse = Invoke-RestMethod -Uri "$baseUrl/api/numbers/assign" -Method POST -Body $assignBody -Headers $headers
                Write-Host "✅ Number assignment successful"
            } catch {
                Write-Host "❌ Number assignment failed: $($_.Exception.Message)"
            }
        }
    } catch {
        Write-Host "❌ Available numbers failed: $($_.Exception.Message)"
    }

    # Test 5: Spectrum scan
    try {
        $spectrumResponse = Invoke-RestMethod -Uri "$baseUrl/api/spectrum/scan" -Method POST -Headers $headers
        Write-Host "✅ Spectrum scan successful: $($spectrumResponse.towers_detected) towers"
    } catch {
        Write-Host "❌ Spectrum scan failed: $($_.Exception.Message)"
    }

} catch {
    Write-Host "❌ Login failed: $($_.Exception.Message)"
}