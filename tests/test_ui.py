from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"

def test_ui_successful_login(page: Page):
    """TC_UI_01: Valid user login redirects to Welcome dashboard"""
    page.goto(BASE_URL)
    
    # Fill login form
    page.fill("#email", "admin@qa.com")
    page.fill("#password", "Pass123!")
    page.click("#login-btn")
    
    # Assertions on Welcome Screen
    expect(page.locator("#welcome-card")).to_be_visible()
    expect(page.locator("#welcome-title")).to_have_text("Welcome Back, Admin!")
    expect(page.locator("#login-card")).to_be_hidden()

def test_ui_invalid_login_toast(page: Page):
    """TC_UI_02: Invalid credentials trigger red toast message"""
    page.goto(BASE_URL)
    
    # Fill form with invalid password
    page.fill("#email", "admin@qa.com")
    page.fill("#password", "WrongPass")
    page.click("#login-btn")
    
    # Assertions on Error Toast
    expect(page.locator("#error-toast")).to_be_visible()
    expect(page.locator("#error-toast")).to_contain_text("Invalid email or password")
    expect(page.locator("#login-card")).to_be_visible()

def test_ui_logout_flow(page: Page):
    """TC_UI_03: Log out button returns user to login form"""
    page.goto(BASE_URL)
    
    # Complete Login
    page.fill("#email", "admin@qa.com")
    page.fill("#password", "Pass123!")
    page.click("#login-btn")
    
    # Click Logout
    page.click("#logout-btn")
    
    # Assertions
    expect(page.locator("#login-card")).to_be_visible()
    expect(page.locator("#welcome-card")).to_be_hidden()