import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Configuration
num_defects = 200
modules = ['Authentication', 'Payment Gateway', 'User Dashboard', 
           'Reporting', 'API Service', 'Database', 
           'Notification System', 'Admin Panel']
severities = ['Critical', 'Major', 'Minor', 'Low']
statuses = ['Open', 'In Progress', 'Resolved', 'Closed', 'Reopened']
priorities = ['High', 'Medium', 'Low']
developers = ['John Doe', 'Jane Smith', 'Mike Johnson', 
              'Sarah Wilson', 'Chris Lee', 'Emily Brown', 
              'David Chen', 'Lisa Anderson']

# Generate defect IDs
defect_ids = [f'DEF-{str(i+1).zfill(4)}' for i in range(num_defects)]

# Generate random data with realistic distributions
defect_modules = np.random.choice(modules, num_defects, 
                                  p=[0.15, 0.20, 0.12, 0.10, 0.18, 0.08, 0.10, 0.07])
defect_severities = np.random.choice(severities, num_defects, 
                                     p=[0.15, 0.30, 0.35, 0.20])
defect_statuses = np.random.choice(statuses, num_defects, 
                                   p=[0.20, 0.15, 0.25, 0.35, 0.05])
defect_priorities = np.random.choice(priorities, num_defects, 
                                     p=[0.25, 0.50, 0.25])
defect_assigned = np.random.choice(developers, num_defects)

# Generate dates
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 27)
date_range = (end_date - start_date).days

reported_dates = [start_date + timedelta(days=np.random.randint(0, date_range)) 
                  for _ in range(num_defects)]

# Generate resolved dates (only for resolved/closed defects)
resolved_dates = []
for i, status in enumerate(defect_statuses):
    if status in ['Resolved', 'Closed']:
        resolution_days = np.random.randint(1, 30) if defect_severities[i] == 'Critical' \
                         else np.random.randint(1, 60)
        resolved_dates.append(reported_dates[i] + timedelta(days=resolution_days))
    else:
        resolved_dates.append(None)

# Create DataFrame
df = pd.DataFrame({
    'defect_id': defect_ids,
    'module': defect_modules,
    'severity': defect_severities,
    'status': defect_statuses,
    'reported_date': reported_dates,
    'resolved_date': resolved_dates,
    'priority': defect_priorities,
    'assigned_to': defect_assigned
})

# Sort by reported date
df = df.sort_values('reported_date').reset_index(drop=True)

# Save to CSV
df.to_csv('defects.csv', index=False)
print("✅ defects.csv created successfully!")
print(f"Generated {len(df)} defect records")
