title: Git commands
slug: git-commands
summary: Git commands
date: 2023-09-30
modified: 2023-09-30
category: Git
status: Draft



## Get code from a tagged release

git clone --branch v0.3 https://github.com/blinklet/usermapper-web.git

## Open new branch using VS Code

* Ctrl-Shift-P
* Git: Create Branch From...
* choose repo
* choose "main" branch
* name the new branch ("newdb") in my case
* Click "Publish Branch" to push it to remote

VSCode now tracks the "newdb" branch. Remember to work in this branch going forward for the database features.

## Go back to main branch to make a minor fix, and then copy fix back into dev branch

* Go to source control pane
* Select the three dots next to repo name
* Checkout to...
* choose "main" branch

make changes

Commit changes to *main* and push changes to GitHub

Then, merge changes to the development branch

(general case, maybe there are other changes in the main repo you need)
Ensure you are in *main* branch

* Go to source control pane
* Select the three dots next to repo name
* Pull

Now you have all changes in *main*

* Go to source control pane
* Select the three dots next to repo name
* Checkout to...
* choose "newdb" branch

* Go to source control pane
* Select the three dots next to repo name
* Branch --> Rebase branch
* Select branch to rebase into
  * Select *main*

See that the changes from *main* now appear in *newdb*. But they don't need to be committed. They are already committed and just need to be pushed to remote branch

* Click Sync Changes

Continue working in *newdb*



# Use Github cli

https://github.com/cli/cli/blob/trunk/docs/install_linux.md

https://cli.github.com/


