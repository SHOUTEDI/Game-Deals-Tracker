import pandas as pd

class ExcelReporter:
    def generate_report(self, dataframe, filename="game_deals_report.xlsx"):
        if dataframe.empty:
            print("No data available to generate report.")
            return
        
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        
        dataframe.to_excel(writer, sheet_name='Game Deals', index=False)
        
        workbook  = writer.book
        worksheet = writer.sheets['Game Deals']
        
        header_fmt = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4F81BD', 
            'font_color': '#FFFFFF',  
        })
        
        money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        percent_fmt = workbook.add_format({'num_format': '0.00%'})
        
        green_fmt = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
        
        for col_num, value in enumerate(dataframe.columns.values):
            worksheet.write(0, col_num, value, header_fmt)
            
        worksheet.set_column('A:A', 40)
        worksheet.set_column('B:C', 15, money_fmt)
        
        worksheet.conditional_format('D2:D100', {
            'type': 'cell',
            'criteria': '>=',
            'value': 70,
            'format': green_fmt
        })
        
        writer.close()
        print(f"Report generated: {filename}")