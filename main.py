from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

app = FastAPI()

# CORS middleware to allow requests from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your React app's URL
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    fruit = Column(String, index=True)
    country = Column(String, index=True)

Base.metadata.create_all(bind=engine)

@app.post("/submit_order/")
async def submit_order(fruit: str = Form(...), country: str = Form(...)):
    order = Order(fruit=fruit, country=country)
    db = SessionLocal()
    db.add(order)
    db.commit()
    db.close()
    
    response_message = f"Order received! You ordered {fruit} from {country}."
    return {"message": response_message}

@app.get("/orders/")
async def get_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    
    orders_list = [{"id": order.id, "fruit": order.fruit, "country": order.country} for order in orders]
    return {"orders": orders_list}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")

async def read_item(item_id: int):
    return {"item_id": item_id}