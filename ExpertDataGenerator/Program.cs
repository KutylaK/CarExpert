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
            byte[] bin = File.ReadAllBytes(@"..\..\..\eksperty.xlsx");

            
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


            var train = new StringBuilder();
            var test = new StringBuilder();
            var headers = excelData[0];
            train.AppendLine(string.Join(",", headers));
            test.AppendLine(string.Join(",", headers));

            var enableMutations = false;
            var limit = 100000;
            var random = new Random((int)DateTime.Now.Ticks);
            for (int i = 0; i < limit ; i++)
            {

                var elemBase = excelData[random.Next(2,excelData.Count)];
                var elem = new string[elemBase.Count];
                elemBase.CopyTo(elem,0);
                var mutationP = new Random((int)DateTime.Now.Ticks).NextDouble();

                if(mutationP < 0.3 && enableMutations)
                {
                    elem[new Random((int)DateTime.Now.Ticks).Next(elem.Count()-1)] = "1";
                }


                if(i<limit*0.8)
                    train.AppendLine(string.Join(",",elem));
                else
                    test.AppendLine(string.Join(",", elem));
                
            }

            var exportHeaders = headers.Take(headers.Count-1).Select(_ => $"'{_}'");
            var exportDiagnosis = excelData.Skip(1).Select(_ => $"'{_.Last()}'");


           

            File.WriteAllText(@"..\..\..\..\CarExpert.App\CarExpert.App\train.csv", train.ToString());
            File.WriteAllText(@"..\..\..\..\CarExpert.App\CarExpert.App\test.csv", test.ToString());
            File.WriteAllText(@"..\..\..\headers.txt", string.Join(",",exportHeaders));
            File.WriteAllText(@"..\..\..\diagnosis.txt", string.Join(",", exportDiagnosis));

        }
    }
}
