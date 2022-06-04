from datetime import datetime
from app import app


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}
