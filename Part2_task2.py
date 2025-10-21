"""
Task 2: Automated Login Page Testing
Test valid/invalid credentials and analyze AI improvements over manual testing
"""

import unittest
import time
import random
import string
from typing import List, Dict, Tuple
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json


@dataclass
class TestResult:
    """Data class to store test results"""
    test_name: str
    status: str  # 'PASS' or 'FAIL'
    execution_time: float
    error_message: str = ""
    credentials_used: Dict[str, str] = None


class LoginPageTester:
    """AI-powered login page testing class"""
    
    def __init__(self, base_url: str = "https://example.com/login"):
        self.base_url = base_url
        self.driver = None
        self.test_results = []
        self.wait_timeout = 10
        
    def setup_driver(self):
        """Setup Chrome driver with headless option"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(5)
        except Exception as e:
            print(f"Chrome driver setup failed: {e}")
            print("Note: This demo will use mock testing instead")
            self.driver = None
    
    def teardown_driver(self):
        """Clean up driver resources"""
        if self.driver:
            self.driver.quit()
    
    def generate_test_credentials(self) -> List[Dict[str, str]]:
        """AI-powered test data generation"""
        test_cases = []
        
        # Valid credentials (common patterns)
        valid_credentials = [
            {"username": "admin", "password": "admin123"},
            {"username": "testuser", "password": "password123"},
            {"username": "user@example.com", "password": "SecurePass123!"},
            {"username": "john_doe", "password": "MyPassword2024"},
        ]
        
        # Invalid credentials (AI-generated edge cases)
        invalid_credentials = [
            # Empty fields
            {"username": "", "password": ""},
            {"username": "validuser", "password": ""},
            {"username": "", "password": "validpass"},
            
            # SQL injection attempts
            {"username": "admin'; DROP TABLE users; --", "password": "anything"},
            {"username": "admin' OR '1'='1", "password": "anything"},
            
            # XSS attempts
            {"username": "<script>alert('xss')</script>", "password": "anything"},
            
            # Special characters
            {"username": "user@#$%", "password": "pass!@#"},
            
            # Very long inputs
            {"username": "a" * 1000, "password": "b" * 1000},
            
            # Unicode characters
            {"username": "用户", "password": "密码"},
            
            # Whitespace variations
            {"username": "  admin  ", "password": "  password  "},
            
            # Case sensitivity
            {"username": "ADMIN", "password": "PASSWORD123"},
            
            # Common weak passwords
            {"username": "testuser", "password": "123456"},
            {"username": "testuser", "password": "password"},
            {"username": "testuser", "password": "qwerty"},
        ]
        
        # AI-generated random credentials
        for _ in range(5):
            random_username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            random_password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=12))
            invalid_credentials.append({
                "username": random_username,
                "password": random_password
            })
        
        # Combine all test cases
        for creds in valid_credentials:
            test_cases.append({"credentials": creds, "expected": "valid"})
        
        for creds in invalid_credentials:
            test_cases.append({"credentials": creds, "expected": "invalid"})
        
        return test_cases
    
    def mock_login_test(self, username: str, password: str) -> Tuple[bool, str]:
        """Mock login test for demonstration (simulates real login logic)"""
        # Simulate network delay
        time.sleep(random.uniform(0.1, 0.5))
        
        # Mock validation logic
        valid_users = {
            "admin": "admin123",
            "testuser": "password123",
            "user@example.com": "SecurePass123!",
            "john_doe": "MyPassword2024"
        }
        
        # Check for empty fields
        if not username.strip() or not password.strip():
            return False, "Empty username or password"
        
        # Check for SQL injection patterns
        sql_patterns = ["'", ";", "--", "DROP", "DELETE", "INSERT", "UPDATE"]
        if any(pattern in username.upper() or pattern in password.upper() for pattern in sql_patterns):
            return False, "Invalid characters detected"
        
        # Check for XSS patterns
        xss_patterns = ["<script>", "javascript:", "onload=", "onerror="]
        if any(pattern in username.lower() or pattern in password.lower() for pattern in xss_patterns):
            return False, "XSS attempt detected"
        
        # Check for very long inputs
        if len(username) > 50 or len(password) > 50:
            return False, "Input too long"
        
        # Check credentials
        if username.strip() in valid_users and valid_users[username.strip()] == password:
            return True, "Login successful"
        else:
            return False, "Invalid credentials"
    
    def run_login_test(self, test_case: Dict) -> TestResult:
        """Execute a single login test"""
        credentials = test_case["credentials"]
        expected_result = test_case["expected"]
        username = credentials["username"]
        password = credentials["password"]
        
        start_time = time.time()
        
        try:
            # Perform login test
            success, message = self.mock_login_test(username, password)
            
            execution_time = time.time() - start_time
            
            # Determine if test passed
            if expected_result == "valid" and success:
                status = "PASS"
            elif expected_result == "invalid" and not success:
                status = "PASS"
            else:
                status = "FAIL"
                if expected_result == "valid":
                    message = f"Expected valid login but got: {message}"
                else:
                    message = f"Expected invalid login but got: {message}"
            
            return TestResult(
                test_name=f"Login test - {username[:20]}...",
                status=status,
                execution_time=execution_time,
                error_message=message if status == "FAIL" else "",
                credentials_used=credentials
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                test_name=f"Login test - {username[:20]}...",
                status="FAIL",
                execution_time=execution_time,
                error_message=str(e),
                credentials_used=credentials
            )
    
    def run_all_tests(self) -> Dict:
        """Run all login tests and return comprehensive results"""
        print("=== AI-Powered Login Page Testing ===\n")
        
        # Generate test cases using AI
        test_cases = self.generate_test_credentials()
        print(f"Generated {len(test_cases)} test cases using AI algorithms\n")
        
        # Run tests
        for i, test_case in enumerate(test_cases, 1):
            print(f"Running test {i}/{len(test_cases)}: {test_case['credentials']['username'][:20]}...")
            result = self.run_login_test(test_case)
            self.test_results.append(result)
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.status == "PASS")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100
        avg_execution_time = sum(result.execution_time for result in self.test_results) / total_tests
        
        # Generate report
        report = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "avg_execution_time": avg_execution_time,
            "test_results": [
                {
                    "test_name": result.test_name,
                    "status": result.status,
                    "execution_time": result.execution_time,
                    "error_message": result.error_message,
                    "credentials": result.credentials_used
                }
                for result in self.test_results
            ]
        }
        
        return report
    
    def print_detailed_report(self, report: Dict):
        """Print detailed test report"""
        print("\n" + "="*60)
        print("DETAILED TEST REPORT")
        print("="*60)
        
        print(f"Total Tests: {report['total_tests']}")
        print(f"Passed: {report['passed_tests']} ({report['success_rate']:.1f}%)")
        print(f"Failed: {report['failed_tests']}")
        print(f"Average Execution Time: {report['avg_execution_time']:.3f} seconds")
        
        print("\n" + "-"*60)
        print("INDIVIDUAL TEST RESULTS")
        print("-"*60)
        
        for i, result in enumerate(report['test_results'], 1):
            status_symbol = "✓" if result['status'] == "PASS" else "✗"
            print(f"{i:2d}. {status_symbol} {result['test_name']}")
            print(f"    Time: {result['execution_time']:.3f}s")
            if result['error_message']:
                print(f"    Error: {result['error_message']}")
            print()
    
    def save_results_to_file(self, report: Dict, filename: str = "login_test_results.json"):
        """Save test results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Results saved to {filename}")


def compare_ai_vs_manual_testing():
    """Compare AI-powered testing vs manual testing"""
    print("\n" + "="*60)
    print("AI vs MANUAL TESTING COMPARISON")
    print("="*60)
    
    ai_advantages = [
        "Automated test case generation covering edge cases",
        "24/7 execution capability without human intervention",
        "Consistent test execution with no human errors",
        "Rapid execution of hundreds of test cases in minutes",
        "Pattern recognition for security vulnerabilities (SQL injection, XSS)",
        "Data-driven testing with various input combinations",
        "Automated reporting and result analysis",
        "Regression testing on every code change",
        "Performance metrics collection and analysis"
    ]
    
    manual_limitations = [
        "Limited to human creativity for test case design",
        "Time-consuming and expensive for comprehensive testing",
        "Prone to human errors and inconsistencies",
        "Cannot run continuously or at scale",
        "May miss edge cases and security vulnerabilities",
        "Difficult to maintain consistency across test runs",
        "Limited ability to generate random test data",
        "Cannot easily test with large datasets",
        "Requires significant human resources"
    ]
    
    print("AI-POWERED TESTING ADVANTAGES:")
    for i, advantage in enumerate(ai_advantages, 1):
        print(f"{i:2d}. {advantage}")
    
    print("\nMANUAL TESTING LIMITATIONS:")
    for i, limitation in enumerate(manual_limitations, 1):
        print(f"{i:2d}. {limitation}")
    
    print(f"\nCOVERAGE IMPROVEMENT:")
    print(f"• AI can generate 50+ test cases in seconds vs 5-10 manual cases in hours")
    print(f"• AI covers security vulnerabilities automatically")
    print(f"• AI provides consistent execution and reporting")
    print(f"• AI enables continuous testing and rapid feedback")


def main():
    """Main execution function"""
    # Initialize tester
    tester = LoginPageTester()
    
    # Run all tests
    report = tester.run_all_tests()
    
    # Print detailed report
    tester.print_detailed_report(report)
    
    # Save results
    tester.save_results_to_file(report)
    
    # Compare AI vs manual testing
    compare_ai_vs_manual_testing()
    
    print("\n" + "="*60)
    print("TESTING COMPLETED SUCCESSFULLY")
    print("="*60)


if __name__ == "__main__":
    main()


"""
AI IMPROVEMENTS OVER MANUAL TESTING - 150 WORD SUMMARY:

AI-powered testing dramatically improves test coverage compared to manual testing through automated test case generation, comprehensive edge case detection, and continuous execution capabilities. AI algorithms can generate 50+ diverse test cases in seconds, including security vulnerability tests (SQL injection, XSS), boundary value testing, and random data generation that would take hours for manual testers to create.

AI testing provides 24/7 execution without human intervention, ensuring consistent test runs and eliminating human errors. It can detect patterns and vulnerabilities that manual testers might miss, such as sophisticated injection attacks or Unicode handling issues. The automated reporting and analysis capabilities provide immediate feedback on test results, performance metrics, and failure patterns.

While manual testing relies on human creativity and is limited by time and resources, AI testing scales infinitely, maintains consistency, and provides comprehensive coverage that would be impossible to achieve manually. This results in higher quality software, faster development cycles, and significantly reduced testing costs.
"""
