# Contribution guide

Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

## Adding a new write-up entry

1. Each CTF gets its own folder in the root of this repository. For example, ‘Foo Bar CTF 2015’ would get a folder named `foo-bar-ctf-2015`.
2. Every CTF challenge gets its own subfolder within that folder with an appendix indicating its value. For example, all files related to the ‘Foo Bar CTF 2015’ challenge named ‘Sucky sandbox’, which is worth `150` points, would be located in `foo-bar-ctf-2015/sucky-sandbox-150`.
3. Every CTF challenge folder needs a Markdown-formatted `README.md` file, e.g. `foo-bar-ctf-2015/sucky-sandbox-150/README.md`. This file contains any details about the challenge, the main write-up itself, and links to other write-ups and resources. The folder should also contain the source files needed to reproduce the challenge.
4. Once you’re done adding the entry or making your changes, submit a pull request using the GitHub web interface.
5. Finally, make sure you follow our committing rules

## Changing an existing entry

1. Feel free to make any changes you see fit. Add a link to a write-up on your blog, add missing source files, clarify explanations in the write-up, or — if you’ve found a better way to solve a challenge — simplify the existing solution.
2. Once you’re done, submit a pull request using the GitHub web interface.

## Committing rules
These rules exist to keep the repo maintainable and complete. Please consider following them.

1. Update the root `big-ctf/README.md` file, when adding a write-up to `big-ctf/task/`. We have three different sections:
	* `Completed write-ups` - Tasks, for which there is at least one local repo write-up (see the `Write-up` section of each task)
	* `External write-ups only` - Tasks, for which there is at least one external write-up (see the `Other write-ups and resources` section of each task, but no local write-up
	* `Missing write-ups` - Tasks, for which there are no write-ups available (yet).
2. If there already exists a write-up in the `Write-up` section and you want to add another local write-up:
	- Add another `Alternative write-up` section above the `Other write-ups and resources` section
3. Do not add files that have a filesize bigger than 15MB to keep the repo relatively small. Upload the file instead to a service or reference it from somewhere else.
4. Consider following these [committing rules](https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages). For this repo, we like to use these [emojis](http://www.emoji-cheat-sheet.com/):
	* :memo: when adding a write-up to the `Write-up` section of a task
	* :floppy_disk: when adding resources for a task, e.g. files or scripts
	* :link: when adding a write-up link to the `Other write-ups and resources` section of a task
	* :pill: when fixing broken links or corrupt Markup stuff
	* :books: when updating the structure of this repo or adding a ctf skeleton structure
	* :fire: when deleting files
5. If you want to add a new CTF directory/structure (skeleton) with as little trouble as possible, then consider using the `genctf.py` tool from [our tools repo](https://github.com/ctfs/write-ups-tools/)
