import cv2
import numpy as np
import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import logging

# Import project modules
from real_time.emotion_detector import EmotionDetector
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Emotion Detection API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = None

@app.on_event("startup")
async def startup_event():
    global detector
    try:
        logger.info("Initializing emotion detector on startup...")
        detector = EmotionDetector()
        logger.info("Emotion detector initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize emotion detector: {e}")
        detector = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": detector is not None}

@app.websocket("/ws/detect")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        logger.info(f"WebSocket connection accepted from {websocket.client}")
        print(f"DEBUG: WebSocket accepted from {websocket.client}")
        
        while True:
            # Receive data from frontend
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if "image" not in message:
                continue
            
            # Decode base64 image
            try:
                image_data = message["image"].split(",")[1]
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as e:
                logger.error(f"Error decoding image: {e}")
                continue
            
            if frame is None:
                continue
            
            # Detect emotions
            if detector:
                try:
                    _, predictions = detector.detect_emotions(frame)
                    
                    # Convert float32 to float for JSON serialization
                    serializable_predictions = []
                    for pred in predictions:
                        serializable_predictions.append({
                            "emotion": pred["emotion"],
                            "confidence": float(pred["confidence"]),
                            "bbox": [int(x) for x in pred["bbox"]]
                        })

                    # Send results back to frontend
                    await websocket.send_json({
                        "predictions": serializable_predictions,
                        "count": len(serializable_predictions)
                    })
                except Exception as e:
                    logger.error(f"Error during detection: {e}")
                    await websocket.send_json({"error": "Detection failed", "predictions": []})
            else:
                await websocket.send_json({
                    "error": "Model not loaded",
                    "predictions": []
                })
                
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed by client")
    except Exception as e:
        logger.error(f"Error in WebSocket communication: {e}")
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
