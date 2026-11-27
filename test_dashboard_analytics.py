import unittest
import pandas as pd
from dashboard.analytics import add_business_metrics,category_summary,validate_dataset
def sample():
    return pd.DataFrame({"Category":["A","A","B"],"Region":["North","South","North"],"Seasonality":["Winter","Winter","Summer"],"Units Sold":[10,0,30],"Inventory Level":[8,0,50],"Demand Forecast":[12,5,20],"Price":[2.,3.,4.]})
class AnalyticsTests(unittest.TestCase):
    def test_schema(self):
        self.assertEqual(validate_dataset(sample()),[])
        self.assertIn("Dataset contains no rows.",validate_dataset(sample().iloc[:0]))
        self.assertTrue(any("Missing required" in x for x in validate_dataset(sample().drop(columns=["Region"]))))
        bad=sample();bad["Price"]=bad["Price"].astype("object");bad.loc[0,"Price"]="bad"
        self.assertTrue(any("non-numeric" in x for x in validate_dataset(bad)))
    def test_forecast_gap_coverage(self):
        out=add_business_metrics(sample())
        self.assertEqual(out["Forecast Gap"].tolist(),[2,5,-10])
        self.assertEqual(out["Inventory Coverage"].iloc[0],round(8/12,2))
        self.assertTrue(pd.isna(out["Forecast Gap %"].iloc[1]))
    def test_inventory_status(self):
        self.assertEqual(add_business_metrics(sample())["Inventory Risk"].tolist(),["Below forecast","Out of stock","At/above forecast"])
    def test_aggregate(self):
        out=category_summary(sample())
        self.assertEqual(out.iloc[0]["Category"],"B")
        self.assertEqual(out.iloc[0]["Units_Sold"],30)
        self.assertEqual(out.iloc[0]["Demand_Forecast"],20)
if __name__=="__main__": unittest.main()
