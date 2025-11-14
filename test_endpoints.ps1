# Comprehensive API Endpoint Test Script
# Tests all endpoints for 404, 422, and proper functionality

$baseUrl = "http://localhost:5000"
$passedTests = 0
$failedTests = 0
$results = @()

function Test-Endpoint {
    param(
        [string]$method,
        [string]$endpoint,
        [int]$expectedStatus,
        [hashtable]$body = $null,
        [string]$token = $null,
        [string]$testName
    )
    
    $url = "$baseUrl$endpoint"
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    if ($token) {
        $headers["Authorization"] = "Bearer $token"
    }
    
    try {
        $params = @{
            Uri = $url
            Method = $method
            Headers = $headers
            UseBasicParsing = $true
        }
        
        if ($body) {
            $params["Body"] = ($body | ConvertTo-Json -Depth 10)
        }
        
        try {
            $response = Invoke-WebRequest @params -ErrorAction Stop
            $statusCode = $response.StatusCode
        }
        catch {
            $statusCode = $_.Exception.Response.StatusCode.Value__
        }
        
        $passed = $statusCode -eq $expectedStatus
        
        if ($passed) {
            Write-Host "[PASS] $testName" -ForegroundColor Green
            $script:passedTests++
        }
        else {
            Write-Host "[FAIL] $testName - Expected $expectedStatus, got $statusCode" -ForegroundColor Red
            $script:failedTests++
        }
        
        $script:results += @{
            TestName = $testName
            Passed = $passed
            Expected = $expectedStatus
            Actual = $statusCode
        }
        
        return @{ StatusCode = $statusCode; Response = $response }
    }
    catch {
        Write-Host "[ERROR] $testName - $($_.Exception.Message)" -ForegroundColor Yellow
        $script:failedTests++
        return $null
    }
}

Write-Host "`n=====================================================================================================" -ForegroundColor Cyan
Write-Host "  COMPREHENSIVE API TEST SUITE" -ForegroundColor Cyan
Write-Host "  Testing: $baseUrl" -ForegroundColor Cyan
Write-Host "====================================================================================================`n" -ForegroundColor Cyan

# Check if server is running
try {
    $testResponse = Invoke-WebRequest -Uri "$baseUrl/safe_zones" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[OK] Server is running`n" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Cannot connect to server at $baseUrl" -ForegroundColor Red
    Write-Host "Make sure the server is running with: python app.py`n" -ForegroundColor Red
    exit 1
}

# Test variables
$testToken = $null
$invalidToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.token"

# ==========================================
# 1. TEST 404 ERRORS
# ==========================================
Write-Host "`n[1] Testing 404 Error Handling" -ForegroundColor Yellow
Test-Endpoint -method "GET" -endpoint "/nonexistent" -expectedStatus 404 -testName "Non-existent endpoint"
Test-Endpoint -method "GET" -endpoint "/api/fake" -expectedStatus 404 -testName "Fake API endpoint"
Test-Endpoint -method "POST" -endpoint "/wrong/path" -expectedStatus 404 -testName "Wrong path POST"

# ==========================================
# 2. TEST AUTHENTICATION
# ==========================================
Write-Host "`n[2] Testing Authentication" -ForegroundColor Yellow

$timestamp = [int][double]::Parse((Get-Date -UFormat %s))
$testEmail = "test_user_$timestamp@example.com"

# Register
$registerData = @{
    name = "Test User"
    email = $testEmail
    password = "testpass123"
    role = "student"
}
$result = Test-Endpoint -method "POST" -endpoint "/auth/register" -expectedStatus 201 -body $registerData -testName "Register new user"

# Login
$loginData = @{
    email = $testEmail
    password = "testpass123"
}
$result = Test-Endpoint -method "POST" -endpoint "/auth/login" -expectedStatus 200 -body $loginData -testName "Login with valid credentials"

if ($result -and $result.StatusCode -eq 200) {
    try {
        $loginResponse = $result.Response.Content | ConvertFrom-Json
        $testToken = $loginResponse.access_token
        Write-Host "  [OK] Got authentication token" -ForegroundColor Green
    }
    catch {
        Write-Host "  [WARN] Could not parse login response" -ForegroundColor Yellow
    }
}

# Login with wrong password
Test-Endpoint -method "POST" -endpoint "/auth/login" -expectedStatus 401 -body @{email=$testEmail; password="wrongpass"} -testName "Login with wrong password"

# Login with missing fields
Test-Endpoint -method "POST" -endpoint "/auth/login" -expectedStatus 400 -body @{email=$testEmail} -testName "Login with missing password"

# ==========================================
# 3. TEST 422 TOKEN ERRORS
# ==========================================
Write-Host "`n[3] Testing 422 Invalid Token Handling" -ForegroundColor Yellow

Test-Endpoint -method "GET" -endpoint "/debug/token" -expectedStatus 422 -token $invalidToken -testName "Protected endpoint with invalid token"
Test-Endpoint -method "GET" -endpoint "/debug/token" -expectedStatus 401 -testName "Protected endpoint without token"

if ($testToken) {
    Test-Endpoint -method "GET" -endpoint "/debug/token" -expectedStatus 200 -token $testToken -testName "Protected endpoint with valid token"
}

# ==========================================
# 4. TEST SAFE ZONES
# ==========================================
Write-Host "`n[4] Testing Safe Zones" -ForegroundColor Yellow

Test-Endpoint -method "GET" -endpoint "/safe_zones" -expectedStatus 200 -testName "Get all safe zones"
Test-Endpoint -method "GET" -endpoint "/safe_zones/99999" -expectedStatus 404 -testName "Get non-existent safe zone"

if ($testToken) {
    $zoneData = @{
        name = "Test Zone"
        latitude = 28.6139
        longitude = 77.2090
        description = "Test zone"
    }
    Test-Endpoint -method "POST" -endpoint "/safe_zones" -expectedStatus 403 -body $zoneData -token $testToken -testName "Create safe zone as student (should fail)"
    Test-Endpoint -method "POST" -endpoint "/safe_zones/1/mark" -expectedStatus 201 -token $testToken -testName "Mark safe zone"
    Test-Endpoint -method "GET" -endpoint "/safe_zones/marked" -expectedStatus 200 -token $testToken -testName "Get marked safe zones"
    Test-Endpoint -method "DELETE" -endpoint "/safe_zones/1/mark" -expectedStatus 200 -token $testToken -testName "Unmark safe zone"
}

# ==========================================
# 5. TEST OTHER ENDPOINTS
# ==========================================
Write-Host "`n[5] Testing Other Endpoints" -ForegroundColor Yellow

Test-Endpoint -method "GET" -endpoint "/disasters" -expectedStatus 200 -testName "Get all disasters"
Test-Endpoint -method "GET" -endpoint "/modules" -expectedStatus 200 -testName "Get all modules"
Test-Endpoint -method "GET" -endpoint "/drills" -expectedStatus 200 -testName "Get all drills"
Test-Endpoint -method "GET" -endpoint "/alerts" -expectedStatus 200 -testName "Get all alerts"
Test-Endpoint -method "GET" -endpoint "/emergency-contacts" -expectedStatus 200 -testName "Get emergency contacts"

if ($testToken) {
    Test-Endpoint -method "GET" -endpoint "/messages/inbox" -expectedStatus 200 -token $testToken -testName "Get message inbox"
    Test-Endpoint -method "GET" -endpoint "/messages/sent" -expectedStatus 200 -token $testToken -testName "Get sent messages"
    Test-Endpoint -method "GET" -endpoint "/achievements/my" -expectedStatus 200 -token $testToken -testName "Get my achievements"
    Test-Endpoint -method "GET" -endpoint "/leaderboard" -expectedStatus 200 -token $testToken -testName "Get leaderboard"
    Test-Endpoint -method "GET" -endpoint "/activities/recent" -expectedStatus 200 -token $testToken -testName "Get recent activities"
}

# ==========================================
# SUMMARY
# ==========================================
Write-Host "`n=====================================================================================================" -ForegroundColor Cyan
Write-Host "  TEST SUMMARY" -ForegroundColor Cyan
Write-Host "====================================================================================================`n" -ForegroundColor Cyan

$totalTests = $passedTests + $failedTests
$passRate = if ($totalTests -gt 0) { ($passedTests / $totalTests * 100) } else { 0 }

Write-Host "Total Tests: $totalTests"
Write-Host "Passed: $passedTests" -ForegroundColor Green
Write-Host "Failed: $failedTests" -ForegroundColor Red
Write-Host ("Pass Rate: {0:N1}%" -f $passRate)

if ($failedTests -eq 0) {
    Write-Host "`n[SUCCESS] All tests passed! The application is working correctly.`n" -ForegroundColor Green
}
else {
    Write-Host "`n[WARNING] Some tests failed. Please review the errors above.`n" -ForegroundColor Yellow
}
