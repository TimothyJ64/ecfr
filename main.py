from fastapi import FastAPI, HTTPException
import httpx
import json
import os

app = FastAPI()

ECFR_TITLES_URL = "https://www.ecfr.gov/api/versioner/v1/titles.json"
OUTPUT_FILE = "titles_details.out"

@app.get("/ecfr/titles")
async def get_and_save_ecfr_titles():
    headers = {"accept": "application/json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ECFR_TITLES_URL, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Save to file
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return {"message": f"Data successfully saved to {OUTPUT_FILE}"}

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

