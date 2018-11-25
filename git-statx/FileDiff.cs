namespace git_statx
{
    public class FileDiff
    {
        public int LinesAdded { get; set; }
        public int LinesDeleted { get; set; }
        public int NumberCommits { get; set; }

        public FileDiff(int LinesAdded, int linesDeleted, int numberCommits)
        {
            this.LinesAdded = LinesAdded;
            LinesDeleted = linesDeleted;
            NumberCommits = numberCommits;
        }
    }
}
