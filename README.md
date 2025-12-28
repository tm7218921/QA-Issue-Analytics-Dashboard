
# QA Defect Analytics Dashboard

A comprehensive data analytics dashboard for Quality Assurance teams to track, analyze, and visualize software defects using Python, Pandas, and Streamlit.

## Features

### Key Metrics
- Total defects count.
- Open vs closed defects with delta indicators.
- Severity breakdown (Critical, Major, Minor, Low).
- Average resolution time in days.

### Interactive Filters
- Filter by severity (Critical, Major, Minor, Low).
- Filter by status (Open, In Progress, Resolved, Closed, Reopened).
- Filter by module or component.
- Date range filter for reported defects.
- Real-time data filtering with live updates.

### Visualizations
1. Bar chart of defects by severity with color-coded severity levels.
2. Pie chart of defect status distribution with percentage breakdown.
3. Line chart of defects reported over time (monthly trend).
4. Horizontal bar chart of top modules with the most defects.
5. High-risk module chart showing critical and high-severity defects.

### Advanced Analytics
- High-risk module analysis highlighting modules with frequent critical or major defects.
- Detailed data table with sorting and filtering.
- CSV upload to use custom defect data.
- Export of filtered data to CSV.
- Professional layout using Streamlit columns, sidebar, and metrics.

## Dataset Schema

The sample `defects.csv` includes the following fields:

| Field         | Type   | Description                                      |
|--------------|--------|--------------------------------------------------|
| defect_id    | String | Unique identifier (for example, DEF-0001)        |
| module       | String | Component or module name                         |
| severity     | String | Critical, Major, Minor, or Low                   |
| status       | String | Open, In Progress, Resolved, Closed, Reopened    |
| reported_date| Date   | Date when the defect was reported                |
| resolved_date| Date   | Date when the defect was resolved (if applicable)|
| priority     | String | High, Medium, or Low                             |
| assigned_to  | String | Developer or team member assigned                |

The sample dataset contains 200 realistic defects across multiple modules for a full year.

## Installation

### Prerequisites
- Python 3.8 or higher.
- pip (Python package manager).

### Setup Instructions

1. Clone the repository:
```
git clone https://github.com/YOUR_USERNAME/qa-defect-analytics-dashboard.git
cd qa-defect-analytics-dashboard
```

2. (Optional) Create and activate a virtual environment:
```
python -m venv venv
venv\Scripts\activate          # Windows
# or
source venv/bin/activate       # macOS/Linux
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

### Run the Dashboard
```
streamlit run app.py
```

The dashboard will be available at:
`http://localhost:8501`

### Using Custom Data
1. Open the dashboard in your browser.
2. Use the sidebar file uploader to upload your own CSV file.
3. Ensure your CSV matches the required schema (same column names and date format).

### Filtering and Exporting
- Use sidebar filters for severity, status, module, and date range.
- The main section will update metrics and charts according to the filters.
- Use the download button to export the filtered data as a CSV file.

## Project Structure

```
qa-defect-analytics-dashboard/
├── app.py              # Main Streamlit application
├── defects.csv         # Sample dataset with 200 defects
├── create_dataset.py   # Script to generate sample dataset
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Technologies Used

- Python 3.x
- Streamlit
- Pandas
- Plotly
- NumPy

## Dashboard Sections

1. Key metrics panel with total defects, open defects, severity counts, and average resolution time.
2. Visualizations:
   - Defects by severity.
   - Defect status distribution.
   - Defects reported over time.
   - Top modules by defect count.
3. High-risk module analysis focusing on critical and major defects.
4. Detailed defect data table with optional full column view and CSV export.

## Use Cases

- Quality assurance teams tracking defect trends.
- Project managers monitoring product quality and defect resolution.
- Developers identifying high-risk modules and prioritizing fixes.
- Portfolio demonstration of data analytics and Streamlit skills.

## Future Enhancements

Potential improvements:
- Database integration instead of CSV files.
- User authentication and role-based access.
- Email or chat notifications for critical defects.
- Predictive analytics for defect trends.
- Integration with external issue trackers such as JIRA or GitHub Issues.

## Contributing

1. Fork the repository.
2. Create a feature branch:
```
git checkout -b feature/your-feature-name
```
3. Commit your changes:
```
git commit -m "Describe your changes"
```
4. Push the branch:
```
git push origin feature/your-feature-name
```
5. Open a pull request.

## License

This project can be used for learning and portfolio purposes. You can optionally add a standard license such as MIT to formalize reuse.

## Author

Replace this section with your own details:

- Name: Your Name
- GitHub: https://github.com/YOUR_USERNAME
- LinkedIn: your LinkedIn profile URL
- Portfolio: your portfolio URL
```You can copy this text directly into `README.md` and then adjust the project name, username, and links to match your GitHub and personal details.

<img width="1765" height="659" alt="Screenshot 2025-12-28 221722" src="https://github.com/user-attachments/assets/ec4df963-7f19-4082-8198-a41ff82b8fd7" />
<img width="1474" height="894" alt="Screenshot 2025-12-28 221732" src="https://github.com/user-attachments/assets/75c19bcd-6df2-4767-bdb5-0b23ace2a6b8" />
<img width="1461" height="690" alt="Screenshot 2025-12-28 221746" src="https://github.com/user-attachments/assets/0a3ccbcc-b87a-456d-8f8d-d1a5157964eb" />
<img width="1449" height="710" alt="Screenshot 2025-12-28 221756" src="https://github.com/user-attachments/assets/a828276c-cb85-4225-a483-d7a05e892d74" />
<img width="1432" height="772" alt="Screenshot 2025-12-28 221808" src="https://github.com/user-attachments/assets/1469070b-4f95-4222-b13b-3bbb5c16fbca" />

