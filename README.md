# git-statx

Generates a CSV which looks like:

| File           | Statistic      | 2018 February | 2018 March | 2018 April | ... |
| -------------- | -------------- | ------------- | ---------- | ---------- | --- |
| .gitignore     | lines added    | 29            | 0          | 0          | 2   |
| .gitignore     | lines deleted  | 6             | 0          | 0          | 0   |
| .gitignore     | number commits | 3             | 0          | 0          | 1   |
| src/Program.cs | lines added    | 102           | 23         | 56         | 123 |
| ...            | ...            | ...           | ...        | ...        | ... |

This application uses [libgit2](http://libgit2.github.com/) via [LibGit2Sharp](https://github.com/libgit2/libgit2sharp).

Note: the performance of this application is significantly worse than `git log --numstat`. A future iteration may switch to capturing console output, rather than using libgit2. 
