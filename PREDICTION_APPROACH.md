# Booking Confirmation Prediction (Machine Learning Logic)

## Overview
This system uses a **Supervised Machine Learning** model to predict the probability that a booking will be successfully confirmed (i.e., not cancelled later). Unlike simple rule-based systems, this approach learns patterns from historical data.

---

## 🤖 The Model: Random Forest Classifier
We utilize `scikit-learn`'s **Random Forest Classifier** to generate predictions.

### Why Random Forest?
- **Non-Linear Relationships**: It can capture complex interactions between features (e.g., booking far in advance might usually be good, but *too* far in advance might indicate uncertain plans).
- **Robustness**: It averages multiple decision trees to reduce overfitting compared to a single decision tree.
- **Probabilistic Output**: It allows us to extract a "confidence score" (`predict_proba`) rather than just a simplistic Yes/No classification.

---

## � Feature Operations (The "Inputs")
The model analyzes the following data points for every booking request:

| Feature | Description | Hypothesis |
| :--- | :--- | :--- |
| **Route Distance** | Absolute difference between Source and Destination station IDs. | Longer trips assume higher commitment from the traveler. |
| **Meal Choice** | Whether the user added a meal (Veg/Non-Veg) or not. | Users who pay for amenities like meals are statistically less likely to cancel. |
| **Days in Advance** | Number of days between booking date and travel date. | Last-minute bookings (Urgent) are high probability. Very early bookings are steady but have higher cancellation variance. |
| **Is Weekend** | Is the travel date a Saturday or Sunday? | Weekend trips are more prone to casual plan changes compared to weekday business travel. |

---

## 📈 Training Methodology (Mock Data)
Since this is a demonstration environment without years of real historical records, we employ a **Synthetic Data Generation** pipeline (`generate_mock_data`):

1. **Simulation**: We generate 2,000+ mock booking records.
2. **Logic Injection**: We assign "Confirmed" outcomes based on probabilistic rules (e.g., higher chance for long distance) mixed with **Gaussian Noise** to simulate real-world unpredictability.
3. **Training**: The model trains on this dataset on startup.
4. **Inference**: When a real user books, the trained model predicts the outcome for *that specific* scenario.

---

## 🧠 Approach Comparison

| Metric | Old Approach (Rule-Based) | New Approach (ML - Random Forest) |
| :--- | :--- | :--- |
| **Logic** | Hardcoded `if/else` statements. | Learned patterns from data. |
| **Scalability** | Hard to maintain as rules get complex. | Automatically improves with more data. |
| **Accuracy** | Fixed and static. | Dynamic and contextual. |
