import os
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    files_to_screenshot = [
        "test-pages/SEIU083_Contract_Enforcement_Team/GrievanceEscalateToStep2.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/GrievanceEscalateToStep3.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Acknowledge_Request_for_a_Steward_of_Record.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Information_Request_Submission_01.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Information_Request_Submission_02_Second_Request_DELR.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Information_Request_Submission_03_Third_Request_AVP-HR.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Information_Request_Submission_04_Fourth_Request_VP-FADM.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Information_Request_Submission_05_Fifth_Request_PO.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Official_Steward_of_Record.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Official_Steward_of_Record_with_Senior_Steward.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_ELR_Removal_Of_Outdated_Records_Request.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_Employee_Notification_Steward_of_Record_Assigned.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_Steward_New_Case_Notification.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_Steward_Notification_Staff_Investigatory_Meeting.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_Steward_Notification_of_Employee_Layoff.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_Steward_Time_Availability_for_a_Case.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_Steward_Time_Availability_for_an_Investigatory_Interview.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/SEIUPSU_Case_Work_out_of_Class_Reclassification_Documentation_Needed.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/Steward_Supervisor_Email_Template_Notice_of_Union_Activity.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/Template_General_Steward_Email.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/WeingartenRightsStatement-CardsTemplate.html",
        "test-pages/SEIU083_Contract_Enforcement_Team/WorkplaceBullyingPoster.html",
    ]

    if not os.path.exists("jules-scratch/verification/screenshots"):
        os.makedirs("jules-scratch/verification/screenshots")

    for file_path in files_to_screenshot:
        abs_path = os.path.abspath(file_path)
        page.goto(f"file://{abs_path}")
        screenshot_path = f"jules-scratch/verification/screenshots/{os.path.basename(file_path)}.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)