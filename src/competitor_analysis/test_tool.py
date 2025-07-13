# test_tool.py
import asyncio
# from src.competitor_analysis.tools.scrape_tool import ScrapeTools # Adjust this import to match your file path
# from crewai_tools import ScrapeWebsiteTool
from competitor_analysis.tools.stagehand_browser_tool import extract_heading_with_stagehand
# A function to run your tool
def run_tool_test():
    print("--- Starting Tool Test ---")
    
    # The URL that causes the issue
    test_url = "https://www.nike.com"
    
    try:
        # Create an instance of your tool class
        # scraping_tool = ScrapeTools()
        
        print(f"Attempting to scrape: {test_url}")
        
        # Call the specific tool method directly
        # Replace 'BrowserBasedOnUrl' with the actual function name if it's different
        print(f"stagehand analysis",extract_heading_with_stagehand("https://nike.com/"))
        
        print("--- Tool Finished Successfully! ---")
        print("\nResult:")
        # Print the first 500 characters of the result
        # print(result[:500] + "...")

    except Exception as e:
        print(f"--- An Error Occurred in the Tool ---")
        print(e)

# --- Run the test ---
if __name__ == "__main__":
    run_tool_test()