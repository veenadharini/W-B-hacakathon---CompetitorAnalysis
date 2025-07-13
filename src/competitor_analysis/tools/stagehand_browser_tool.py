# # tools/stagehand_tool.py

# import requests

# def extract_heading_with_stagehand(url: str) -> str:
#     """
#     Calls the local Stagehand API server to extract the main heading from the page.
#     """
#     try:
#         response = requests.post(
#             "http://localhost:8000/extract-product-data",
#             json={"url": url},
#             timeout=60
#         )
#         data = response.json()

#         if data.get("status") == "success":
#             return f"✅ Heading: {data['result']}"
#         else:
#             return f"❌ API Error: {data.get('message')}"

#     except Exception as e:
#         return f"❌ Failed to contact Stagehand API: {e}"

# tools/stagehand_tool.py

import requests
from crewai.tools.base_tool import BaseTool

# Define a class that inherits from BaseTool. This is the most reliable way.
class StagehandHeadingExtractorTool(BaseTool):
    name: str = "Stagehand Heading Extractor"
    description: str = "Extracts the main heading from a given website URL. You must pass the full URL as the input to this tool."

    def _run(self, url: str) -> str:
        """The internal method that executes the tool's logic."""
        try:
            print(f"📥 Stagehand tool received URL: {url}")
            response = requests.post(
                "http://localhost:8000/extract-product-data",
                json={"url": url},
                timeout=60
            )
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            print(f"📤 Stagehand tool response: {data}")
            if data.get("status") == "success":
                return f"✅ Heading: {data['result']}"
            else:
                return f"❌ API Error: {data.get('message')}"

        except requests.exceptions.RequestException as e:
            return f"❌ Failed to contact Stagehand API: {e}"
        except Exception as e:
            return f"❌ An unexpected error occurred: {e}"