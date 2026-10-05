from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .data import DATA

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

def percentile(values, p):
    values = sorted(values)
    
    if not values:
        return 0.0

    pos = (len(values) - 1) * (p / 100)
    lower = int(pos)
    upper = min(lower + 1, len(values) - 1)

    if lower == upper :
        return values[lower]
    
    frac = pos - lower

    return values[lower] + (values[upper] - values[lower]) * frac

@app.get('/')
def root():
    return {"message": "Hello, World!"}

@app.post('/api/latency')
async def get_latency_mat(request: Request):
    body = await request.json()
    
    regions = body['regions']
    threshold_ms = body['threshold_ms']

    result = []

    for region in regions:
        
        rows = [
            record for record in DATA
            if record['region'] == region
        ]

        if not rows:
            continue 
        
        latencies = [r['latency_ms'] for r in rows]
        uptimes = [r['uptime_pct'] for r in rows]

        result.append({
            "region": region,
            "avg_latency": round(sum(latencies) / len(latencies), 2),
            "p95_latency": round(percentile(latencies, 95), 2),
            "avg_uptime": round(sum(uptimes) / len(uptimes), 3),
            "breaches": sum(1 for l in latencies if l > threshold_ms)
        })

    return {'regions': result}

