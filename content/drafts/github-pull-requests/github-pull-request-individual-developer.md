Using GitHub pull requests as an individual developer

Instead of putting all my thoughts in my blog, document development in pull requests

I can write everything I learn in the pull request documentation

Provides a history of what I did that I can read. All in-line with my project



https://www.tempertemper.net/blog/why-i-always-raise-a-pull-request-on-solo-projects

https://docs.github.com/en/pull-requests

https://softwareengineering.stackexchange.com/questions/178402/is-there-a-purpose-for-using-pull-requests-on-my-own-repo-if-i-am-the-only-devel

https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models

https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/best-practices-for-pull-requests


Lifecycle of a change

- every change has its own branch
- a pull request is associated with a branch

- create issue (there will be many issues in my backlog after a while)
  - record my thoughts about what needs to change
  - pick an issue to work on
  - create a branch for the issue. You need to have a branch in order to create a pull request

- in local repo, run following commands to get branch from GitHub remote

```
git fetch remote
git checkout 1-confirm-or-cancel-spreadsheet-import-to-database
```

- You can't create a pull request until there are changes in the new branch. So it would be best to add implementation comments to the *issue* while working on it

- Create the pull request when the code is finished in the branch
  - See all the changes made in the branch
    - I like to create a pull request becaise i will record my implementation in it and also record what I learned
      - This makes the Issue and the PR a good basis for a "draft" blog post of I decide to write about what I learned
  - link pull request to the issue
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue

- Merge the PR, which will automatically close the issue
- ensure changes are synced back to my local repo
- delete the branch in both local and remote

- 