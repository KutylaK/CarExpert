using OfficeOpenXml;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace ExpertDataGenerator
{
    class Program
    {
        static void Main(string[] args)
        {
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
            //create a list to hold all the values
            List<List<string>> excelData = new List<List<string>>();

            //read the Excel file as byte array
            byte[] bin = File.ReadAllBytes(@"C:\Users\KutylaK\Desktop\eksperty.xlsx");

            
            //create a new Excel package in a memorystream
            using (MemoryStream stream = new MemoryStream(bin))
            using (ExcelPackage excelPackage = new ExcelPackage(stream))
            {
                //loop all worksheets
                foreach (ExcelWorksheet worksheet in excelPackage.Workbook.Worksheets)
                {
                    //loop all rows
                    for (int i = worksheet.Dimension.Start.Row; i <= worksheet.Dimension.End.Row; i++)
                    {
                        var row = new List<string>();
                        //loop all columns in a row
                        for (int j = worksheet.Dimension.Start.Column; j <= worksheet.Dimension.End.Column; j++)
                        {
                            //add the cell data to the List
                            if (worksheet.Cells[i, j].Value != null)
                            {
                                row.Add(worksheet.Cells[i, j].Value.ToString());
                            }
                        }
                        excelData.Add(row);
                    }
                }
            }


            var sb = new StringBuilder();
            var headers = excelData[0];
            sb.AppendLine(string.Join(",", headers));

            var random = new Random((int)DateTime.Now.Ticks);
            for (int i = 0; i < 10000; i++)
            {

                var elemBase = excelData[random.Next(2,excelData.Count)];
                var elem = new string[elemBase.Count];
                elemBase.CopyTo(elem,0);
                var mutationP = new Random((int)DateTime.Now.Ticks).NextDouble();

                if(mutationP < 0.3)
                {
                    elem[new Random((int)DateTime.Now.Ticks).Next(elem.Count()-1)] = "1";
                }
                sb.AppendLine(string.Join(",",elem));
            }

            var exportHeaders = headers.Take(headers.Count-1).Select(_ => $"'{_}'");
            var exportDiagnosis = excelData.Skip(1).Select(_ => $"'{_.Last()}'");

            File.WriteAllText(@"C:\Users\KutylaK\source\repos\ExpertDataGenerator\ExpertDataGenerator\data.csv", sb.ToString());
            File.WriteAllText(@"C:\Users\KutylaK\source\repos\ExpertDataGenerator\ExpertDataGenerator\headers.txt", string.Join(",",exportHeaders));
            File.WriteAllText(@"C:\Users\KutylaK\source\repos\ExpertDataGenerator\ExpertDataGenerator\diagnosis.txt", string.Join(",", exportDiagnosis));

        }
    }
}
