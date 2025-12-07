import pandas as pd

class PersonalFinanceAgent:
    def __init__(self, file_path, salary=50000):
        self.salary = salary
        self.df = pd.read_excel(file_path)
        
        self.df.columns = self.df.columns.str.strip()
    
    def monthly_summary(self):
        print("\n=== 🏦 Monthly Salary vs Expenses ===")
        summary = self.df.groupby("Month")["Amount"].sum()
        for month, total in summary.items():
            savings = self.salary - total
            status = "❌ Deficit" if savings < 0 else "✅ Savings"
            print(f"{month:10} | Salary: ₹{self.salary:7} | Expenses: ₹{total:7} | Savings: ₹{savings:7} → {status}")
        return summary
    
    def category_breakdown(self):
        print("\n=== 📊 Category-wise Breakdown ===")
        breakdown = self.df.groupby(["Month", "Category"])["Amount"].sum().reset_index()
        
        current_month = None
        monthly_total = 0
        for _, row in breakdown.iterrows():
            if row["Month"] != current_month:
                # print totals for previous month before switching
                if current_month is not None:
                    savings = self.salary - monthly_total
                    status = "❌ Deficit" if savings < 0 else "✅ Savings"
                    print(f"   -----------------------------")
                    print(f"   Total Expenses : ₹{monthly_total}")
                    print(f"   Savings        : ₹{savings} → {status}\n")
                
                # reset for new month
                current_month = row["Month"]
                monthly_total = 0
                print(f"\n{current_month}")
            
            # print each category
            print(f"   {row['Category']:12} : ₹{row['Amount']}")
            monthly_total += row["Amount"]
        
        savings = self.salary - monthly_total
        status = "❌ Deficit" if savings < 0 else "✅ Savings"
        print(f"   -----------------------------")
        print(f"   Total Expenses : ₹{monthly_total}")
        print(f"   Savings        : ₹{savings} → {status}\n")
        
        return breakdown
    
    def advisor(self):
        print("\n=== 🤖 AI Agent Advice ===")
        monthly = self.df.groupby("Month")["Amount"].sum()
        for month, total in monthly.items():
            if total > self.salary:
                print(f"⚠️ {month}: You overspent by ₹{total - self.salary}. Cut down on non-essential categories.")
            else:
                print(f"✅ {month}: You saved ₹{self.salary - total}. Consider investing this amount.")
        
       
        total_expense = self.df["Amount"].sum()
        shopping_total = self.df[self.df["Category"] == "Shopping"]["Amount"].sum()
        entertainment_total = self.df[self.df["Category"] == "Entertainment"]["Amount"].sum()
        
        if shopping_total > 0.25 * total_expense:
            print("⚠️ Too much shopping! Try setting a shopping budget.")
        if entertainment_total > 0.2 * total_expense:
            print("⚠️ Entertainment expenses are high! Look for cheaper/free alternatives.")
    
    def run(self):
        self.monthly_summary()
        self.category_breakdown()
        self.advisor()



if __name__ == "__main__":
    file_path = "Personal_Finance_Tracker_5Months.xlsx"  # keep Excel file in same folder
    agent = PersonalFinanceAgent(file_path, salary=50000)
    agent.run()
