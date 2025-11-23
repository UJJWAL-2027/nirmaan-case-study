# Run locally - Detailed steps

## Prerequisites
- Python 3.8+
- pip
- (Optional) GPU for faster sentence-transformers, otherwise CPU works.

## Steps
1. Clone the repo or copy files.
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows (PowerShell)
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
   Note: `sentence-transformers` will download a model (~80-120MB). If you cannot download models (air-gapped), the scorer will fall back to a neutral semantic score.
4. Run the app:
   ```bash
   python app.py
   ```
5. Open `http://localhost:8080` in your browser. Paste transcript and click Score.
6. To call programmatically (example using curl):
   ```bash
   curl -X POST -F 'transcript=<PASTE TRANSCRIPT>' http://localhost:8080/score
   ```

## Deployment
- This demo is suitable for quick deployment to any small VM (AWS EC2 free tier, Render, Railway).
- Ensure you set `HOST=0.0.0.0` and open the port (8080 by default).
- For production, add error handling, rate-limiting, and optionally cache embeddings.

## Limitations & Notes
- The semantic component requires `sentence-transformers` and internet access to download the model.
- The rubric-reading expects columns like `criterion`, `description`, `keywords`, `weight`, `min_words`, `max_words` in the provided Excel file.
- This is a demo scaffold to show product thinking; you may extend it with richer feedback, audio handling, or more advanced models.
