# Retail Intelligence Platform

An interactive analytics dashboard for exploring retail sales, inventory, product, and demand-related data. The project demonstrates how data preparation and visualization can support business reporting.

## Screenshots\n\n![Category sales](<screenshots/category wise sales.png.png>)\n\n![Region sales](<screenshots/region wise seles.png.png>)\n\n![Demand vs units sold](<screenshots/df vs us.png.png>)\n\n![Inventory and insights](<screenshots/investery status & business insights.png.png>)\n\n## Dashboard capabilities

- Retail KPI summaries
- Sales performance analysis
- Category and region comparisons
- Inventory-level exploration
- Category-aggregated sales vs. demand forecast comparisons\n- Forecast gap and forecast-gap percentage indicators\n- Inventory coverage and risk flags (out of stock / below forecast / at-or-above forecast)\n- Adjustable low-stock threshold
- Filters and dataset exploration
- Interactive visual reporting

## Tech stack

Python · Streamlit · Pandas

## Data

The project expects a retail inventory dataset with fields covering stores, products, inventory, sales, demand forecasts, pricing, discounts, regions, seasonal patterns, and competitor prices. Check the `data/` folder and dashboard code for the exact columns used.

## Run locally

```bash
git clone https://github.com/Madhum4107/Retail-Intelligence-Platform.git
cd Retail-Intelligence-Platform
python -m venv .venv
```

Activate:

**Windows**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install and launch:

```bash
python -m pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Repository structure

```
├── dashboard/     # Dashboard application
├── data/          # Dataset(s)
├── notebooks/     # Exploratory work
├── screenshots/   # Visual previews
└── requirements.txt
```

## Future ideas

- More robust forecasting evaluation
- Inventory risk and replenishment recommendations
- Data-quality checks
- Exportable business reports
- Deployment and automated tests

## Author

**Madhumitha M** · AI & ML student

[GitHub](https://github.com/Madhum4107) · [LinkedIn](https://www.linkedin.com/in/madhumitha4107/)
