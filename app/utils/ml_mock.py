import random
import pandas as pd
import numpy as np
from datetime import date
from sklearn.ensemble import RandomForestClassifier

# Global variable to hold the trained model
_model = None

def generate_mock_data(n_samples=2000):
    """
    Generates mock historical data for training the ML model.
    Simulates features derived from booking details and assigns a target 'confirmed' status
    based on probabilistic rules + noise.
    """
    data = []
    for _ in range(n_samples):
        # Feature: Distance (Station difference)
        dist = random.randint(1, 10) 
        
        # Feature: Meal Choice (0=No, 1=Yes)
        has_meal = random.choice([0, 1])
        
        # Feature: Days Reserved in Advance
        days_advance = random.randint(0, 45)
        
        # Feature: Is Weekend (0=Weekday, 1=Weekend)
        is_weekend = random.choice([0, 1])
        
        # --- Logic to assign Target "confirmed" (0 or 1) ---
        # Base log-odds
        # Longer distance -> Higher commitment -> Higher confirmation
        # Meal selected -> Higher commitment -> Higher confirmation
        # Very late booking (0 days) -> High confirmation (urgent)
        # Very early booking (>30 days) -> Moderate confirmation
        # Weekend -> Slightly more cancellations (change of plans)
        
        score = 0.0
        score += dist * 0.15          # Distance bonus
        score += has_meal * 0.6       # Meal bonus
        score += -0.2 if is_weekend else 0.1
        
        # Days advance non-linear: 
        # 0-3 days: High conf.
        # 3-14 days: Medium.
        # >14 days: Slightly lower (plans change).
        if days_advance < 3:
            score += 0.5
        elif days_advance > 14:
            score -= 0.2
            
        # Add random noise
        score += np.random.normal(0, 0.5)
        
        # Convert to probability (sigmoid) and then binary outcome
        prob = 1 / (1 + np.exp(-score))
        
        # Simulate the actual outcome
        is_confirmed = 1 if random.random() < prob else 0
        
        data.append({
            "distance": dist,
            "has_meal": has_meal,
            "days_advance": days_advance,
            "is_weekend": is_weekend,
            "confirmed": is_confirmed
        })
        
    return pd.DataFrame(data)

def train_model():
    """
    Trains the Random Forest model on generated mock data.
    """
    global _model
    if _model is not None:
        return _model
        
    print("Training ML Model on Mock Data...")
    df = generate_mock_data()
    
    X = df[["distance", "has_meal", "days_advance", "is_weekend"]]
    y = df["confirmed"]
    
    # Simple Random Forest
    clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    clf.fit(X, y)
    
    _model = clf
    print("Model trained.")
    return _model

def predict_confirmation(booking_details) -> float:
    """
    Predicts the probability (0-100%) that a booking will be CONFIRMED.
    Uses a Machine Learning model trained on historical data.
    """
    model = train_model()
    
    # 1. Extract Features from booking_details
    
    # Distance: Abs difference between station IDs
    dist = abs(booking_details.dest_station_id - booking_details.source_station_id)
    
    # Meal: 1 if selected, else 0
    # Assuming booking_details.meal_choice is a string like "Veg", "Non-Veg", "None", or None
    if booking_details.meal_choice and str(booking_details.meal_choice).lower() != "none" and str(booking_details.meal_choice).strip() != "":
        has_meal = 1
    else:
        has_meal = 0
        
    # Days Advance
    # Compare travel_date with today
    # Note: booking_details.travel_date is expected to be a date object
    today = date.today()
    if hasattr(booking_details, "travel_date") and booking_details.travel_date:
        delta = (booking_details.travel_date - today).days
        days_advance = max(0, delta)
    else:
        days_advance = 0 # Default if missing
        
    # Is Weekend
    if hasattr(booking_details, "travel_date") and booking_details.travel_date:
        # 5=Saturday, 6=Sunday
        is_weekend = 1 if booking_details.travel_date.weekday() >= 5 else 0
    else:
        is_weekend = 0

    # 2. Basic Validations (e.g. if source == dest, prob is 0)
    if dist == 0:
        return 0.0

    # 3. Create DataFrame for Prediction
    input_data = pd.DataFrame([{
        "distance": dist,
        "has_meal": has_meal,
        "days_advance": days_advance,
        "is_weekend": is_weekend
    }])
    
    # 4. Predict Probability (for class 1: Confirmed)
    prob_success = model.predict_proba(input_data)[0][1]
    
    # Return as percentage
    return round(prob_success * 100, 2)
