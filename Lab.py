import sys
import sqlite3
import aiosqlite

import websockets
import asyncio
import json

url = "wss://stream.binancefuture.com/ws/bnbusdt@aggTrade"

async def save_down(url):
    
    trades_buffer = []
    while True:
        async with websockets.connect(url) as websocket:
            data = await websocket.recv()
            data = json.loads(data)
            trades_buffer.append(
                (data['a'], data['T'], data['q'], data['p'])
            )
            
            print(data)
            
            if len(trades_buffer) > 3:
                print("Writing to DB!")
                
                async with aiosqlite.connect("./data.db") as db:
                    
                    await db.executemany(""" INSERT INTO trades 
                                        (id, time, quantity, price) VALUES (?, ?, ?, ?)""",
                                        trades_buffer)
                    await db.commit()
                
                trades_buffer = []
        
asyncio.run(save_down(url))

