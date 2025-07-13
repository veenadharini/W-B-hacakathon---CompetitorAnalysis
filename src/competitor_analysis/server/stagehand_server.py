# stagehand_server/server.py

from fastapi import FastAPI
from pydantic import BaseModel
from stagehand import Stagehand, StagehandConfig
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

app = FastAPI()

class ExtractRequest(BaseModel):
    url: str

@app.post("/extract-product-data")
async def extract_product_data(req: ExtractRequest):
    config = StagehandConfig(
        env="BROWSERBASE",
        api_key=os.getenv("BROWSERBASE_API_KEY"),
        project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
        model_name="gpt-4o",
        model_api_key=os.getenv("OPENAI_API_KEY")
    )

    stagehand = Stagehand(config)

    try:
        await stagehand.init()
        page = stagehand.page

        await page.goto(req.url)

        # More informative scraping prompt
        result = await page.extract(
            """
            You are a senior digital analyst with expertise in web strategy, UX, SEO, and competitor benchmarking. Analyze the website: [insert website URL here]. Your task is to provide a detailed breakdown including:

            Overview of the website's purpose and audience.

            Key features, UX elements, and content strategy.

            Technical performance (e.g., load speed, mobile-friendliness, SEO basics).

            Marketing and branding positioning.

            Key insights on strengths, weaknesses, and growth opportunities.

            If the website belongs to a well-known company or brand (e.g., nike.com), then additionally:

            Identify the 3 to 5 main competitors.

            Compare them in a table using these criteria: traffic estimates, product range, pricing level, SEO authority score, social media presence, and unique selling proposition (USP).

            Highlight key insights based on these comparisons.

            Present all results in a structured, professional tone, and include a final executive summary of the most important insights.
            """
        )

        return {"status": "success", "result": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        await stagehand.close()
