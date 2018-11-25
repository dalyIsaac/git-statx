using LibGit2Sharp;
using System;
using System.Collections.Generic;
using System.Linq;

namespace git_statx
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Enter the repo path: ");
            string path = Console.ReadLine().Trim();
            Console.Write("Enter the log path: ");
            string logpath = Console.ReadLine().Trim();
            GetData(path, logpath);
        }

        static void GetData(string path, string logpath)
        {
            try
            {
                using (Repository repo = new Repository(path))
                {
                    DiffTimeContainer diffs = new DiffTimeContainer();
                    Dictionary<string, FileDiff> monthDiffs = new Dictionary<string, FileDiff>();
                    Commit previousCommit = null;

                    diffs.CheckLogPath(logpath);

                    Console.WriteLine("Gathering diffs...");

                    foreach (Commit commit in repo.Commits.QueryBy(new CommitFilter { SortBy = CommitSortStrategies.Time | CommitSortStrategies.Reverse }))
                    {
                        if (commit.Parents.Count() <= 1)
                        {
                            if (previousCommit != null && ((commit.Committer.When.Year == previousCommit.Committer.When.Year && commit.Committer.When.Month > previousCommit.Committer.When.Month) || commit.Committer.When.Year > previousCommit.Committer.When.Year))
                            {
                                monthDiffs = diffs.AddMonthToDiffs(monthDiffs, previousCommit.Committer.When);
                            }

                            // comparison
                            Commit commitTo = repo.Lookup<Commit>(commit.Id);
                            Commit commitFrom = previousCommit != null ? repo.Lookup<Commit>(previousCommit.Id) : null;
                            Patch patch = repo.Diff.Compare<Patch>(commitFrom?.Tree, commitTo.Tree);

                            foreach (PatchEntryChanges pec in patch)
                            {
                                if (monthDiffs.ContainsKey(pec.Path))
                                {
                                    monthDiffs[pec.Path].LinesAdded += pec.LinesAdded;
                                    monthDiffs[pec.Path].LinesDeleted += pec.LinesDeleted;
                                    monthDiffs[pec.Path].NumberCommits += 1;
                                }
                                else
                                {
                                    monthDiffs.Add(pec.Path, new FileDiff(pec.LinesAdded, pec.LinesDeleted, 1));
                                }
                            }
                            if (previousCommit == null)
                            {
                                diffs.FirstDate = commit.Committer.When;
                            }
                            previousCommit = commit;
                        }
                    }
                    monthDiffs = diffs.AddMonthToDiffs(monthDiffs, previousCommit.Committer.When);
                    diffs.ExportCSV(logpath);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
    }
}
