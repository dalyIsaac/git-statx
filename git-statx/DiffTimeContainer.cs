using CsvHelper;
using System;
using System.Collections.Generic;
using System.IO;

namespace git_statx
{
    public class DiffTimeContainer
    {
        public DateTimeOffset FirstDate { get; set; }
        public DateTimeOffset LastDate { get; set; }
        private int _Length;
        public int Length { get { return _Length; } }
        private void IncrementLength()
        {
            _Length += 1;
        }
        public Dictionary<string, List<FileDiff>> diffs = new Dictionary<string, List<FileDiff>>();

        private void AddMissingMonths(DateTimeOffset date)
        {
            IncrementLength();
            int monthDiff = ((date.Year - LastDate.Year) * 12) + date.Month - LastDate.Month;
            foreach (var key in diffs.Keys)
            {
                for (int i = 0; i < monthDiff; i++)
                {
                    diffs[key].Add(new FileDiff(0, 0, 0));
                }
            }
        }

        public Dictionary<string, FileDiff> AddMonthToDiffs(Dictionary<string, FileDiff> monthDiffs, DateTimeOffset date)
        {
            AddMissingMonths(date);

            // existing paths
            foreach (var key in diffs.Keys)
            {
                if (monthDiffs.ContainsKey(key))
                {
                    diffs[key][diffs[key].Count - 1] = monthDiffs[key];
                    monthDiffs.Remove(key);
                }
                else
                {
                    diffs[key][diffs[key].Count - 1] = new FileDiff(0, 0, 0);
                }
            }

            // new paths
            foreach (var key in monthDiffs.Keys)
            {
                diffs[key] = new List<FileDiff>();
                for (int i = 0; i < _Length; i++)
                {
                    diffs[key].Add(new FileDiff(0, 0, 0));
                }
                diffs[key][diffs[key].Count - 1] = monthDiffs[key];
            }
            LastDate = date;

            Console.WriteLine(date.Date.ToString("Y"));
            return new Dictionary<string, FileDiff>();
        }

        public void CheckLogPath(string logpath)
        {
            using (var file = File.Create(logpath))
            {
                var textWriter = new StreamWriter(file);
                var csv = new CsvWriter(textWriter);
            }
        }

        public void ExportCSV(string filename)
        {
            Console.WriteLine($"Writing to {filename}");
            using (var file = File.Create(filename))
            {
                var textWriter = new StreamWriter(file);
                var csv = new CsvWriter(textWriter);

                WriteHeader(csv);
                WriteValues(csv);

                csv.Flush();
                textWriter.Flush();
            }
            Console.WriteLine("Finished writing");
        }

        private void WriteHeader(CsvWriter csv)
        {
            csv.WriteField("File");
            csv.WriteField("Statistic");
            var currentDate = new DateTime(FirstDate.Year, FirstDate.Month, 1);
            var targetDate = new DateTime(LastDate.Year, LastDate.Month, 1);

            while (currentDate <= targetDate)
            {
                csv.WriteField(currentDate.ToString("Y"));
                currentDate = currentDate.AddMonths(1);
            }
            csv.NextRecord();
        }

        private void WriteValues(CsvWriter csv)
        {
            foreach (var key in diffs.Keys)
            {
                var log = diffs[key];

                var linesAdded = new List<int>();
                var linesDeleted = new List<int>();
                var numberCommits = new List<int>();

                for (int i = 0; i < Length; i++)
                {
                    linesAdded.Add(log[i].LinesAdded);
                    linesDeleted.Add(log[i].LinesDeleted);
                    numberCommits.Add(log[i].NumberCommits);
                }


                WriteRecord(csv, key, "lines added", linesAdded);
                WriteRecord(csv, key, "lines deleted", linesDeleted);
                WriteRecord(csv, key, "number commits", numberCommits);
            }
        }

        private void WriteRecord(CsvWriter csv, string key, string statistic, List<int> values)
        {
            csv.WriteField(key);
            csv.WriteField(statistic);
            csv.WriteField(values);
            csv.NextRecord();
        }
    }
}
