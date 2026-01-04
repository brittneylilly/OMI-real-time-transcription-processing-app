from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.post("/webhook")
async def webhook(request: Request):
    # Parse request body
    body = await request.json()
    
    # Print full request body for debugging
    print("=" * 80)
    print("🔍 Full Request Data:")
    print(body)
    print("=" * 80)

    #uid = body.get("uid", "unknown")
    # Get uid from query parameter instead of body
    # Get segments directly from body (not nested in transcript)
    uid = request.query_params.get("uid", "unknown")
    segments = body.get("segments", [])

    print(f"👤 User ID: {uid}")
    print(f"📝 Segments: {segments}")

    # Hint: The transcript contains segments with text data
    # Hint: Access the latest segment with transcript["segments"][-1]["text"]
    # Hint: Return a dictionary with a "message" key and the value being the notification message

    # Task: Implement keyword detection and response logic of your choice
    # example: if the word "tired" is mentioned, return a message notifying the user to take a break

    # TODO: Write your code below this line
    
    # Get the latest transcript segment text
    # if transcript and "segments" in transcript and len(transcript["segments"]) > 0:
    #     latest_text = transcript["segments"][-1]["text"].lower()
    if segments and len(segments) > 0:
        latest_text = segments[-1]["text"].lower()
        print(f"Latest text (lowercase): {latest_text}")
        
        # Define keyword categories and their responses
        keywords_map = {
            # Wellness keywords
            "tired": "💤 You mentioned feeling tired. Consider taking a short break to recharge!",
            "exhausted": "😴 You sound exhausted. Maybe it's time for some rest?",
            "stressed": "🧘 Feeling stressed? Take a deep breath and consider a short meditation break.",
            "anxious": "💆 Anxiety detected. Remember to breathe and take things one step at a time.",
            
            # Health keywords
            "headache": "🤕 Headache mentioned. Stay hydrated and consider taking a break from screens.",
            "sick": "🤒 Hope you feel better soon! Make sure to rest and stay hydrated.",
            "hungry": "🍎 Time for a healthy snack or meal? Your brain needs fuel!",
            "thirsty": "💧 Don't forget to hydrate! Water is essential for focus and energy.",
            
            # Productivity keywords
            "meeting": "📅 Meeting detected. Make sure you're prepared and have your notes ready!",
            "deadline": "⏰ Deadline mentioned. Stay focused and prioritize your tasks!",
            "busy": "📊 Sounds like you're busy. Remember to take breaks to maintain productivity.",
            
            # Positive keywords
            "excited": "🎉 Great to hear your excitement! Keep that positive energy going!",
            "happy": "😊 Wonderful! Positive emotions boost creativity and productivity!",
            "accomplished": "🏆 Amazing work! Celebrate your accomplishments!",
            
            # Learning keywords
            "confused": "🤔 Feeling confused? Break down the problem into smaller parts.",
            "learning": "📚 Keep learning! Every new skill makes you more valuable.",
            "stuck": "💡 Stuck on something? Try explaining it to someone else or take a fresh look later.",
        }
        
        # Check for keywords and return appropriate message
        for keyword, message in keywords_map.items():
            if keyword in latest_text:
                print(f"✅ Found keyword: '{keyword}'")
                print(f"📤 Preparing to return message: {message}")
                
                # Build response
                response_data = {
                    "message": message
                }
                
                print(f"📦 Returning response:")
                print(f"   JSON: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                print(f"   Response Type: application/json")
                print("=" * 80)
                
                # Use JSONResponse to ensure correct Content-Type
                return JSONResponse(
                    content=response_data,
                    status_code=200,
                    headers={"Content-Type": "application/json"}
                )
        
        # Default response if no keywords detected
        print("⚠️ No keywords found")
        print("📦 Returning empty message")
        print("=" * 80)
        return JSONResponse(
            content={"message": ""},
            status_code=200
        )
    
    # Return empty message if no transcript data
    print("❌ No valid transcript data")
    print("=" * 80)
    return JSONResponse(
        content={"message": ""},
        status_code=200
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
