"""Reusable analytics helpers for the retail dashboard."""
import pandas as pd
REQUIRED_COLUMNS={"Category","Region","Seasonality","Units Sold","Inventory Level","Demand Forecast","Price"}
def validate_dataset(frame):
    errors=[]
    if frame.empty: errors.append("Dataset contains no rows.")
    missing=REQUIRED_COLUMNS-set(frame.columns)
    if missing: errors.append("Missing required columns: "+", ".join(sorted(missing)))
    for col in ["Units Sold","Inventory Level","Demand Forecast","Price"]:
        if col in frame:
            numeric=pd.to_numeric(frame[col],errors="coerce")
            invalid=frame[col].notna() & numeric.isna()
            if invalid.any(): errors.append(f"{col} contains {int(invalid.sum())} non-numeric value(s).")
    return errors
def add_business_metrics(frame):
    out=frame.copy()
    out["Forecast Gap"]=pd.to_numeric(out["Demand Forecast"],errors="coerce")-pd.to_numeric(out["Units Sold"],errors="coerce")
    sales=pd.to_numeric(out["Units Sold"],errors="coerce")
    forecast=pd.to_numeric(out["Demand Forecast"],errors="coerce")
    out["Forecast Gap %"]=(out["Forecast Gap"]/sales.replace(0,pd.NA)*100).round(2)
    out["Inventory Coverage"]=(pd.to_numeric(out["Inventory Level"],errors="coerce")/forecast.replace(0,pd.NA)).round(2)
    out["Inventory Risk"]=pd.Series("Review",index=out.index,dtype="string")
    out.loc[out["Inventory Level"]<=0,"Inventory Risk"]="Out of stock"
    out.loc[(out["Inventory Level"]>0)&(out["Inventory Level"]<forecast),"Inventory Risk"]="Below forecast"
    out.loc[out["Inventory Level"]>=forecast,"Inventory Risk"]="At/above forecast"
    return out
def category_summary(frame):
    return frame.groupby("Category",dropna=False,as_index=False).agg(Units_Sold=("Units Sold","sum"),Demand_Forecast=("Demand Forecast","sum"),Inventory=("Inventory Level","sum"),Avg_Price=("Price","mean")).sort_values("Units_Sold",ascending=False)
