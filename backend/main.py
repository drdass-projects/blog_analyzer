from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
# from fetcher import fetch_blogs
from enhanced_fetcher import fetch_blogs
from analyzer import analyze_blogs
from excel_writer import save_to_excel
from mongo_writer import save_to_mongo
import os
from dotenv import load_dotenv
from fastapi import HTTPException



load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fetch-and-analyze")
def fetch_and_analyze(
    keyword: str = Query(..., min_length=2),
    filename: str = Query(None)
):
    try:
        print(f"🔍 Keyword: {keyword}")
        blogs = fetch_blogs(keyword)
        print(f"📥 Blogs fetched: {len(blogs)}")

        if not blogs:
            return {"error": "No blogs found."}

        analyzed_blogs = analyze_blogs(blogs)
        save_to_mongo(keyword, analyzed_blogs)

        if filename and filename.strip():
            safe_filename = f"blogs_{filename.strip().lower().replace(' ', '_')}.xlsx"
        else:
            safe_filename = f"blogs_{keyword.lower().replace(' ', '_')}.xlsx"

        save_to_excel(analyzed_blogs, safe_filename)
        print(f"✅ Saved to {safe_filename}")

        return {
            "file_name": safe_filename,
            "total_blogs": len(analyzed_blogs)
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Internal server error: {str(e)}"}

@app.get("/{file_name}")
def download_file(file_name: str):
    path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(path):
        return FileResponse(
            path,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=file_name
        )
    return {"error": "File not found"}
