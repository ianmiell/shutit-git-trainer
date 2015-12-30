"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class git_trainer(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches) 
		#                                    - Returns True if any lines in output match any of 
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		# 
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of 
		#                                      regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#                                    - Delete text from file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#                                    - Replace text from file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#                                    - Get input from user and return output
		# shutit.fail(msg)                   - Fail the program and exit with status 1
		# 
		shutit.install('git')
		shutit.send('mkdir git-tutorial && cd git-tutorial',note='Make a directory for our first repository and move into it.')
		shutit.send('git init',note='Initialise our git repository')
		shutit.send('ls .git',note='A .git directory has been created, with a file HEAD and two directories (objects and refs).\n\nThe file called head is similar to a symboilc link and points to refs/heads/master (which does not exist yet).\n\nobjects contains the real data of your project, and refs contains references to these data.\n\nThe special master head is the default branch, which is why the .git/HEAD file was created points to it even if it does not yet exist. Basically, the HEAD link is supposed to always point to the branch you are working on right now, and you always start out expecting to work on the master branch. An advanced user may want to take a look at gitrepository-layout(5) after finishing this tutorial.')
		shutit.send('ls .git/refs',note='refs contains references to any number of different heads of development (branches) and to any tags for specific versions you create.')

		#POPULATING A GIT REPOSITORY
		shutit.send('''echo "Hello World" > hello && echo "Silly example" > example''',note='Start off with just creating any random files that you want to maintain in your Git repository. We will start off with a few bad examples, just to get a feel for how this works')
		shutit.send('ls',note='You have now created two files in your working tree (aka working directory), but to actually check in your hard work, you will have to go through two steps: 1) fill in the index file (aka cache) with the information about your working tree state. 2) commit that index file as an object.')
		shutit.send('git update-index --add hello example',note='The first step is trivial: when you want to tell Git about any changes to your working tree, you use the git update-index program. That program normally just takes a list of filenames you want to update, but to avoid trivial mistakes, it refuses to add new entries to the index (or remove existing ones) unless you explicitly tell it that you are adding a new entry with the --add flag (or removing an entry with the --remove) flag.')
		shutit.send('ls .git/objects/??/*',note='You have now told Git to track those two files. In fact, as you did that, if you now look into your object directory, you will notice that Git will have added two new objects to the object database. The numbers after the objects directory (and ignoring the "/" characters) constitute the SHA-1 reference id in the git history.')
		shutit.send(r'''FILE1=$(ls .git/objects/??/* | head -1 | sed 's/.*\([0-9][0-9]\)\/\([0-9]*\)/\1\2/')''')
		shutit.send('git cat-file -t $FILE1',note='If you want to, you can use git cat-file to look at those objects, but you will have to use the object name, not the filename of the object. The -t tells git cat-file to tell you what the "type" of the object is. Git will tell you that you have a "blob" object (ie just a regular file)')
		shutit.send('git cat-file blob $FILE1',note='You can see the contents with a cat-file subcommand, but normally you would not do this.')
		shutit.send('ls .git/index',note='You now have an index file which describes your current working tree. Note that we have not committed or checked anything in yet, we have just made git aware of it.')
		shutit.send('''echo "It's a new day for git" >> hello''',note='Add a line to hello')
		shutit.send('''git diff-files''',note='Show an internal representation of the diff between what has changed compared to the index. Not readable!')
		shutit.send('''git diff-files -p''',note='Show a patch-able diff between what has changed compared to the index.')
		shutit.send('''git diff''',note='git diff does the same thing.')

		#COMMITTING GIT STATE
		tree_id = shutit.send_and_get_output('git write-tree',note='Take the files in the index, and commit them as a so-called tree. It will output the name of the resulting tree.')
		shutit.send('git cat-file -t ' + tree_id,note='This time the object created is not a blob, but a tree object.')
		shutit.send('git cat-file tree ' + tree_id,note='This time the output of the file is less comprehensible.')
		shutit.send('tree=$(git write-tree)',note='We will do that again, but store the tree id in an environment variable.')
		shutit.send('commit=$(echo commit | git commit-tree $tree)',note='Now use the commit-tree command, which normally takes three arguments: the parent commit id (not required here as there is no parent), the tree id we just created, and commit message, which we pipe in.')
		shutit.send('git update-ref HEAD $commit',note='Now we tell git that the HEAD of the tree should point to the commit we just made.')
		shutit.send('git commit',note='The above three commands can be shortened to "git commit".')

		#MAKING A CHANGE
		shutit.send('git diff-files -p',note='The change we made earlier was not committed, as we did not tell the index of the change. It is still there in our local files, but not on the index.')
		shutit.send('git diff-index -p HEAD',note='We can diff our working tree against the index with this command.')
		shutit.send('git diff-index --cached -p HEAD',note='Ignore the working tree and just compare the index with the HEAD using this command.')
		shutit.send('git diff HEAD',note='This is a shorthand version of the same.')
		shutit.send('git update-index hello',note='We need to tell git about the files that have changed. We do not need the --add flag this time, as git knows about the file already.')
		shutit.send('git diff-files -p',note='git diff-files now shows no difference, since the working tree is up to date with the index.')
		shutit.send('git diff-index -p HEAD',note='''We can diff our working tree against the index with this command.\n\n
Here is an ASCII art by Jon Loeliger that illustrates how various diff-* commands compare things.

                diff-tree
                 +----+
                 |    |
                 |    |
                 V    V
              +-----------+
              | Object DB |
              |  Backing  |
              |   Store   |
              +-----------+
                ^    ^
                |    |
                |    |  diff-index --cached
                |    |
    diff-index  |    V
                |  +-----------+
                |  |   Index   |
                |  |  "cache"  |
                |  +-----------+
                |    ^
                |    |
                |    |  diff-files
                |    |
                V    V
              +-----------+
              |  Working  |
              | Directory |
              +-----------+
''')
		shutit.send('git commit -m "New commit"',note='Use the shorthand git commit to commit a new tree and move the HEAD along. -m to add a message')
		#INSPECTING CHANGES
		shutit.send('git rev-list HEAD',note='List the tree references in the repository.')
		shutit.send('git log',note='TODO')
		#In fact, together with the git rev-list program (which generates a list of revisions), git diff-tree ends up being a veritable fount of changes. You can emulate git log, git log -p, etc. with a trivial script that pipes the output of git rev-list to git diff-tree --stdin, which was exactly how early versions of git log were implemented.
		shutit.send('git rev-list | git diff tree --stdin --pretty',note='')
		
		#TAGGING A VERSION
		shutit.send('git tag my-first-tag',note='')
		shutit.send('',note='')
		shutit.send('',note='')
		shutit.send('',note='')
		shutit.send('',note='')
		shutit.send('',note='')
		shutit.send('',note='')
		shutit.send('',note='')
		shutit.send('',note='')
		shutit.send('',note='')
#In Git, there are two kinds of tags, a "light" one, and an "annotated tag".
#
#A "light" tag is technically nothing more than a branch, except we put it in the .git/refs/tags/ subdirectory instead of calling it a head. So the simplest form
#of tag involves nothing more than
#
#    $ git tag my-first-tag
#
#which just writes the current HEAD into the .git/refs/tags/my-first-tag file, after which point you can then use this symbolic name for that particular state. You
#can, for example, do
#
#    $ git diff my-first-tag
#
#to diff your current state against that tag which at this point will obviously be an empty diff, but if you continue to develop and commit stuff, you can use your
#tag as an "anchor-point" to see what has changed since you tagged it.
#
#An "annotated tag" is actually a real Git object, and contains not only a pointer to the state you want to tag, but also a small tag name and message, along with
#optionally a PGP signature that says that yes, you really did that tag. You create these annotated tags with either the -a or -s flag to git tag:
#
#    $ git tag -s <tagname>
#
#which will sign the current HEAD (but you can also give it another argument that specifies the thing to tag, e.g., you could have tagged the current mybranch
#point by using git tag <tagname> mybranch).
#
#You normally only do signed tags for major releases or things like that, while the light-weight tags are useful for any marking you want to do - any time you
#decide that you want to remember a certain point, just create a private tag for it, and you have a nice symbolic name for the state at that point.
#
#COPYING REPOSITORIES
#Git repositories are normally totally self-sufficient and relocatable. Unlike CVS, for example, there is no separate notion of "repository" and "working tree". A
#Git repository normally is the working tree, with the local Git information hidden in the .git subdirectory. There is nothing else. What you see is what you got.
#
#    Note
#    You can tell Git to split the Git internal information from the directory that it tracks, but we'll ignore that for now: it's not how normal projects work,
#    and it's really only meant for special uses. So the mental model of "the Git information is always tied directly to the working tree that it describes" may
#    not be technically 100% accurate, but it's a good model for all normal use.
#
#This has two implications:
#
#   if you grow bored with the tutorial repository you created (or you've made a mistake and want to start all over), you can just do simple
#
#        $ rm -rf git-tutorial
#
#    and it will be gone. There's no external repository, and there's no history outside the project you created.
#
#   if you want to move or duplicate a Git repository, you can do so. There is git clone command, but if all you want to do is just to create a copy of your
#    repository (with all the full history that went along with it), you can do so with a regular cp -a git-tutorial new-git-tutorial.
#
#    Note that when you've moved or copied a Git repository, your Git index file (which caches various information, notably some of the "stat" information for the
#    files involved) will likely need to be refreshed. So after you do a cp -a to create a new copy, you'll want to do
#
#        $ git update-index --refresh
#
#    in the new repository to make sure that the index file is up-to-date.
#
#Note that the second point is true even across machines. You can duplicate a remote Git repository with any regular copy mechanism, be it scp, rsync or wget.
#
#When copying a remote repository, you'll want to at a minimum update the index cache when you do this, and especially with other peoples' repositories you often
#want to make sure that the index cache is in some known state (you don't know what they've done and not yet checked in), so usually you'll precede the git
#update-index with a
#
#    $ git read-tree --reset HEAD
#    $ git update-index --refresh
#
#which will force a total index re-build from the tree pointed to by HEAD. It resets the index contents to HEAD, and then the git update-index makes sure to match
#up all index entries with the checked-out files. If the original repository had uncommitted changes in its working tree, git update-index --refresh notices them
#and tells you they need to be updated.
#
#The above can also be written as simply
#
#    $ git reset
#
#and in fact a lot of the common Git command combinations can be scripted with the git xyz interfaces. You can learn things by just looking at what the various git
#scripts do. For example, git reset used to be the above two lines implemented in git reset, but some things like git status and git commit are slightly more
#complex scripts around the basic Git commands.
#
#Many (most?) public remote repositories will not contain any of the checked out files or even an index file, and will only contain the actual core Git files. Such
#a repository usually doesn't even have the .git subdirectory, but has all the Git files directly in the repository.
#
#To create your own local live copy of such a "raw" Git repository, you'd first create your own subdirectory for the project, and then copy the raw repository
#contents into the .git directory. For example, to create your own copy of the Git repository, you'd do the following
#
#    $ mkdir my-git
#    $ cd my-git
#    $ rsync -rL rsync://rsync.kernel.org/pub/scm/git/git.git/ .git
#
#followed by
#
#    $ git read-tree HEAD
#
#to populate the index. However, now you have populated the index, and you have all the Git internal files, but you will notice that you don't actually have any of
#the working tree files to work on. To get those, you'd check them out with
#
#    $ git checkout-index -u -a
#
#where the -u flag means that you want the checkout to keep the index up-to-date (so that you don't have to refresh it afterward), and the -a flag means "check out
#all files" (if you have a stale copy or an older version of a checked out tree you may also need to add the -f flag first, to tell git checkout-index to force
#overwriting of any old files).
#
#Again, this can all be simplified with
#
#    $ git clone rsync://rsync.kernel.org/pub/scm/git/git.git/ my-git
#    $ cd my-git
#    $ git checkout
#
#which will end up doing all of the above for you.
#
#You have now successfully copied somebody else's (mine) remote repository, and checked it out.
#
#CREATING A NEW BRANCH
#Branches in Git are really nothing more than pointers into the Git object database from within the .git/refs/ subdirectory, and as we already discussed, the HEAD
#branch is nothing but a symlink to one of these object pointers.
#
#You can at any time create a new branch by just picking an arbitrary point in the project history, and just writing the SHA-1 name of that object into a file
#under .git/refs/heads/. You can use any filename you want (and indeed, subdirectories), but the convention is that the "normal" branch is called master. That's
#just a convention, though, and nothing enforces it.
#
#To show that as an example, let's go back to the git-tutorial repository we used earlier, and create a branch in it. You do that by simply just saying that you
#want to check out a new branch:
#
#    $ git checkout -b mybranch
#
#will create a new branch based at the current HEAD position, and switch to it.
#
#    Note
#    If you make the decision to start your new branch at some other point in the history than the current HEAD, you can do so by just telling git checkout what
#    the base of the checkout would be. In other words, if you have an earlier tag or branch, you'd just do
#
#        $ git checkout -b mybranch earlier-commit
#
#    and it would create the new branch mybranch at the earlier commit, and check out the state at that time.
#
#You can always just jump back to your original master branch by doing
#
#    $ git checkout master
#
#(or any other branch-name, for that matter) and if you forget which branch you happen to be on, a simple
#
#    $ cat .git/HEAD
#
#will tell you where it's pointing. To get the list of branches you have, you can say
#
#    $ git branch
#
#which used to be nothing more than a simple script around ls .git/refs/heads. There will be an asterisk in front of the branch you are currently on.
#
#Sometimes you may wish to create a new branch without actually checking it out and switching to it. If so, just use the command
#
#    $ git branch <branchname> [startingpoint]
#
#which will simply create the branch, but will not do anything further. You can then later - once you decide that you want to actually develop on that branch -
#switch to that branch with a regular git checkout with the branchname as the argument.
#
#MERGING TWO BRANCHES
#One of the ideas of having a branch is that you do some (possibly experimental) work in it, and eventually merge it back to the main branch. So assuming you
#created the above mybranch that started out being the same as the original master branch, let's make sure we're in that branch, and do some work there.
#
#    $ git checkout mybranch
#    $ echo "Work, work, work" >>hello
#    $ git commit -m "Some work." -i hello
#
#Here, we just added another line to hello, and we used a shorthand for doing both git update-index hello and git commit by just giving the filename directly to
#git commit, with an -i flag (it tells Git to include that file in addition to what you have done to the index file so far when making the commit). The -m flag is
#to give the commit log message from the command line.
#
#Now, to make it a bit more interesting, let's assume that somebody else does some work in the original branch, and simulate that by going back to the master
#branch, and editing the same file differently there:
#
#    $ git checkout master
#
#Here, take a moment to look at the contents of hello, and notice how they don't contain the work we just did in mybranch - because that work hasn't happened in
#the master branch at all. Then do
#
#    $ echo "Play, play, play" >>hello
#    $ echo "Lots of fun" >>example
#    $ git commit -m "Some fun." -i hello example
#
#since the master branch is obviously in a much better mood.
#
#Now, you've got two branches, and you decide that you want to merge the work done. Before we do that, let's introduce a cool graphical tool that helps you view
#what's going on:
#
#    $ gitk --all
#
#will show you graphically both of your branches (that's what the --all means: normally it will just show you your current HEAD) and their histories. You can also
#see exactly how they came to be from a common source.
#
#Anyway, let's exit gitk (^Q or the File menu), and decide that we want to merge the work we did on the mybranch branch into the master branch (which is currently
#our HEAD too). To do that, there's a nice script called git merge, which wants to know which branches you want to resolve and what the merge is all about:
#
#    $ git merge -m "Merge work in mybranch" mybranch
#
#where the first argument is going to be used as the commit message if the merge can be resolved automatically.
#
#Now, in this case we've intentionally created a situation where the merge will need to be fixed up by hand, though, so Git will do as much of it as it can
#automatically (which in this case is just merge the example file, which had no differences in the mybranch branch), and say:
#
#            Auto-merging hello
#            CONFLICT (content): Merge conflict in hello
#            Automatic merge failed; fix conflicts and then commit the result.
#
#It tells you that it did an "Automatic merge", which failed due to conflicts in hello.
#
#Not to worry. It left the (trivial) conflict in hello in the same form you should already be well used to if you've ever used CVS, so let's just open hello in our
#editor (whatever that may be), and fix it up somehow. I'd suggest just making it so that hello contains all four lines:
#
#    Hello World
#    It's a new day for git
#    Play, play, play
#    Work, work, work
#
#and once you're happy with your manual merge, just do a
#
#    $ git commit -i hello
#
#which will very loudly warn you that you're now committing a merge (which is correct, so never mind), and you can write a small merge message about your
#adventures in git merge-land.
#
#After you're done, start up gitk --all to see graphically what the history looks like. Notice that mybranch still exists, and you can switch to it, and continue
#to work with it if you want to. The mybranch branch will not contain the merge, but next time you merge it from the master branch, Git will know how you merged
#it, so you'll not have to do that merge again.
#
#Another useful tool, especially if you do not always work in X-Window environment, is git show-branch.
#
#    $ git show-branch --topo-order --more=1 master mybranch
#    * [master] Merge work in mybranch
#     ! [mybranch] Some work.
#    --
#    -  [master] Merge work in mybranch
#    *+ [mybranch] Some work.
#    *  [master^] Some fun.
#
#The first two lines indicate that it is showing the two branches with the titles of their top-of-the-tree commits, you are currently on master branch (notice the
#asterisk * character), and the first column for the later output lines is used to show commits contained in the master branch, and the second column for the
#mybranch branch. Three commits are shown along with their titles. All of them have non blank characters in the first column (* shows an ordinary commit on the
#current branch, - is a merge commit), which means they are now part of the master branch. Only the "Some work" commit has the plus + character in the second
#column, because mybranch has not been merged to incorporate these commits from the master branch. The string inside brackets before the commit log message is a
#short name you can use to name the commit. In the above example, master and mybranch are branch heads. master^ is the first parent of master branch head. Please
#see gitrevisions(7) if you want to see more complex cases.
#
#    Note
#    Without the --more=1 option, git show-branch would not output the [master^] commit, as [mybranch] commit is a common ancestor of both master and mybranch
#    tips. Please see git-show-branch(1) for details.
#
#    Note
#    If there were more commits on the master branch after the merge, the merge commit itself would not be shown by git show-branch by default. You would need to
#    provide --sparse option to make the merge commit visible in this case.
#
#Now, let's pretend you are the one who did all the work in mybranch, and the fruit of your hard work has finally been merged to the master branch. Let's go back
#to mybranch, and run git merge to get the "upstream changes" back to your branch.
#
#    $ git checkout mybranch
#    $ git merge -m "Merge upstream changes." master
#
#This outputs something like this (the actual commit object names would be different)
#
#    Updating from ae3a2da... to a80b4aa....
#    Fast-forward (no commit created; -m option ignored)
#     example | 1 +
#     hello   | 1 +
#     2 files changed, 2 insertions(+)
#
#Because your branch did not contain anything more than what had already been merged into the master branch, the merge operation did not actually do a merge.
#Instead, it just updated the top of the tree of your branch to that of the master branch. This is often called fast-forward merge.
#
#You can run gitk --all again to see how the commit ancestry looks like, or run show-branch, which tells you this.
#
#    $ git show-branch master mybranch
#    ! [master] Merge work in mybranch
#     * [mybranch] Merge work in mybranch
#    --
#    -- [master] Merge work in mybranch
#
#MERGING EXTERNAL WORK
#It's usually much more common that you merge with somebody else than merging with your own branches, so it's worth pointing out that Git makes that very easy too,
#and in fact, it's not that different from doing a git merge. In fact, a remote merge ends up being nothing more than "fetch the work from a remote repository into
#a temporary tag" followed by a git merge.
#
#Fetching from a remote repository is done by, unsurprisingly, git fetch:
#
#    $ git fetch <remote-repository>
#
#One of the following transports can be used to name the repository to download from:
#
#Rsync
#    rsync://remote.machine/path/to/repo.git/
#
#    Rsync transport is usable for both uploading and downloading, but is completely unaware of what git does, and can produce unexpected results when you download
#    from the public repository while the repository owner is uploading into it via rsync transport. Most notably, it could update the files under refs/ which
#    holds the object name of the topmost commits before uploading the files in objects/ - the downloader would obtain head commit object name while that object
#    itself is still not available in the repository. For this reason, it is considered deprecated.
#
#SSH
#    remote.machine:/path/to/repo.git/ or
#
#    ssh://remote.machine/path/to/repo.git/
#
#    This transport can be used for both uploading and downloading, and requires you to have a log-in privilege over ssh to the remote machine. It finds out the
#    set of objects the other side lacks by exchanging the head commits both ends have and transfers (close to) minimum set of objects. It is by far the most
#    efficient way to exchange Git objects between repositories.
#
#Local directory
#    /path/to/repo.git/
#
#    This transport is the same as SSH transport but uses sh to run both ends on the local machine instead of running other end on the remote machine via ssh.
#
#Git Native
#    git://remote.machine/path/to/repo.git/
#
#    This transport was designed for anonymous downloading. Like SSH transport, it finds out the set of objects the downstream side lacks and transfers (close to)
#    minimum set of objects.
#
#HTTP(S)
#    http://remote.machine/path/to/repo.git/
#
#    Downloader from http and https URL first obtains the topmost commit object name from the remote site by looking at the specified refname under repo.git/refs/
#    directory, and then tries to obtain the commit object by downloading from repo.git/objects/xx/xxx...  using the object name of that commit object. Then it
#    reads the commit object to find out its parent commits and the associate tree object; it repeats this process until it gets all the necessary objects. Because
#    of this behavior, they are sometimes also called commit walkers.
#
#    The commit walkers are sometimes also called dumb transports, because they do not require any Git aware smart server like Git Native transport does. Any stock
#    HTTP server that does not even support directory index would suffice. But you must prepare your repository with git update-server-info to help dumb transport
#    downloaders.
#
#Once you fetch from the remote repository, you merge that with your current branch.
#
#However - it's such a common thing to fetch and then immediately merge, that it's called git pull, and you can simply do
#
#    $ git pull <remote-repository>
#
#and optionally give a branch-name for the remote end as a second argument.
#
#    Note
#    You could do without using any branches at all, by keeping as many local repositories as you would like to have branches, and merging between them with git
#    pull, just like you merge between branches. The advantage of this approach is that it lets you keep a set of files for each branch checked out and you may
#    find it easier to switch back and forth if you juggle multiple lines of development simultaneously. Of course, you will pay the price of more disk usage to
#    hold multiple working trees, but disk space is cheap these days.
#
#It is likely that you will be pulling from the same remote repository from time to time. As a short hand, you can store the remote repository URL in the local
#repository's config file like this:
#
#    $ git config remote.linus.url http://www.kernel.org/pub/scm/git/git.git/
#
#and use the "linus" keyword with git pull instead of the full URL.
#
#Examples.
#
# 1. git pull linus
#
# 2. git pull linus tag v0.99.1
#
#the above are equivalent to:
#
# 1. git pull http://www.kernel.org/pub/scm/git/git.git/ HEAD
#
# 2. git pull http://www.kernel.org/pub/scm/git/git.git/ tag v0.99.1
#
#HOW DOES THE MERGE WORK?
#We said this tutorial shows what plumbing does to help you cope with the porcelain that isn't flushing, but we so far did not talk about how the merge really
#works. If you are following this tutorial the first time, I'd suggest to skip to "Publishing your work" section and come back here later.
#
#OK, still with me? To give us an example to look at, let's go back to the earlier repository with "hello" and "example" file, and bring ourselves back to the
#pre-merge state:
#
#    $ git show-branch --more=2 master mybranch
#    ! [master] Merge work in mybranch
#     * [mybranch] Merge work in mybranch
#    --
#    -- [master] Merge work in mybranch
#    +* [master^2] Some work.
#    +* [master^] Some fun.
#
#Remember, before running git merge, our master head was at "Some fun." commit, while our mybranch head was at "Some work." commit.
#
#    $ git checkout mybranch
#    $ git reset --hard master^2
#    $ git checkout master
#    $ git reset --hard master^
#
#After rewinding, the commit structure should look like this:
#
#    $ git show-branch
#    * [master] Some fun.
#     ! [mybranch] Some work.
#    --
#    *  [master] Some fun.
#     + [mybranch] Some work.
#    *+ [master^] Initial commit
#
#Now we are ready to experiment with the merge by hand.
#
#git merge command, when merging two branches, uses 3-way merge algorithm. First, it finds the common ancestor between them. The command it uses is git merge-base:
#
#    $ mb=$(git merge-base HEAD mybranch)
#
#The command writes the commit object name of the common ancestor to the standard output, so we captured its output to a variable, because we will be using it in
#the next step. By the way, the common ancestor commit is the "Initial commit" commit in this case. You can tell it by:
#
#    $ git name-rev --name-only --tags $mb
#    my-first-tag
#
#After finding out a common ancestor commit, the second step is this:
#
#    $ git read-tree -m -u $mb HEAD mybranch
#
#This is the same git read-tree command we have already seen, but it takes three trees, unlike previous examples. This reads the contents of each tree into
#different stage in the index file (the first tree goes to stage 1, the second to stage 2, etc.). After reading three trees into three stages, the paths that are
#the same in all three stages are collapsed into stage 0. Also paths that are the same in two of three stages are collapsed into stage 0, taking the SHA-1 from
#either stage 2 or stage 3, whichever is different from stage 1 (i.e. only one side changed from the common ancestor).
#
#After collapsing operation, paths that are different in three trees are left in non-zero stages. At this point, you can inspect the index file with this command:
#
#    $ git ls-files --stage
#    100644 7f8b141b65fdcee47321e399a2598a235a032422 0       example
#    100644 557db03de997c86a4a028e1ebd3a1ceb225be238 1       hello
#    100644 ba42a2a96e3027f3333e13ede4ccf4498c3ae942 2       hello
#    100644 cc44c73eb783565da5831b4d820c962954019b69 3       hello
#
#In our example of only two files, we did not have unchanged files so only example resulted in collapsing. But in real-life large projects, when only a small
#number of files change in one commit, this collapsing tends to trivially merge most of the paths fairly quickly, leaving only a handful of real changes in
#non-zero stages.
#
#To look at only non-zero stages, use --unmerged flag:
#
#    $ git ls-files --unmerged
#    100644 557db03de997c86a4a028e1ebd3a1ceb225be238 1       hello
#    100644 ba42a2a96e3027f3333e13ede4ccf4498c3ae942 2       hello
#    100644 cc44c73eb783565da5831b4d820c962954019b69 3       hello
#
#The next step of merging is to merge these three versions of the file, using 3-way merge. This is done by giving git merge-one-file command as one of the
#arguments to git merge-index command:
#
#    $ git merge-index git-merge-one-file hello
#    Auto-merging hello
#    ERROR: Merge conflict in hello
#    fatal: merge program failed
#
#git merge-one-file script is called with parameters to describe those three versions, and is responsible to leave the merge results in the working tree. It is a
#fairly straightforward shell script, and eventually calls merge program from RCS suite to perform a file-level 3-way merge. In this case, merge detects conflicts,
#and the merge result with conflict marks is left in the working tree.. This can be seen if you run ls-files --stage again at this point:
#
#    $ git ls-files --stage
#    100644 7f8b141b65fdcee47321e399a2598a235a032422 0       example
#    100644 557db03de997c86a4a028e1ebd3a1ceb225be238 1       hello
#    100644 ba42a2a96e3027f3333e13ede4ccf4498c3ae942 2       hello
#    100644 cc44c73eb783565da5831b4d820c962954019b69 3       hello
#
#This is the state of the index file and the working file after git merge returns control back to you, leaving the conflicting merge for you to resolve. Notice
#that the path hello is still unmerged, and what you see with git diff at this point is differences since stage 2 (i.e. your version).
#
#PUBLISHING YOUR WORK
#So, we can use somebody else's work from a remote repository, but how can you prepare a repository to let other people pull from it?
#
#You do your real work in your working tree that has your primary repository hanging under it as its .git subdirectory. You could make that repository accessible
#remotely and ask people to pull from it, but in practice that is not the way things are usually done. A recommended way is to have a public repository, make it
#reachable by other people, and when the changes you made in your primary working tree are in good shape, update the public repository from it. This is often
#called pushing.
#
#    Note
#    This public repository could further be mirrored, and that is how Git repositories at kernel.org are managed.
#
#Publishing the changes from your local (private) repository to your remote (public) repository requires a write privilege on the remote machine. You need to have
#an SSH account there to run a single command, git-receive-pack.
#
#First, you need to create an empty repository on the remote machine that will house your public repository. This empty repository will be populated and be kept
#up-to-date by pushing into it later. Obviously, this repository creation needs to be done only once.
#
#    Note
#    git push uses a pair of commands, git send-pack on your local machine, and git-receive-pack on the remote machine. The communication between the two over the
#    network internally uses an SSH connection.
#
#Your private repository's Git directory is usually .git, but your public repository is often named after the project name, i.e. <project>.git. Let's create such a
#public repository for project my-git. After logging into the remote machine, create an empty directory:
#
#    $ mkdir my-git.git
#
#Then, make that directory into a Git repository by running git init, but this time, since its name is not the usual .git, we do things slightly differently:
#
#    $ GIT_DIR=my-git.git git init
#
#Make sure this directory is available for others you want your changes to be pulled via the transport of your choice. Also you need to make sure that you have the
#git-receive-pack program on the $PATH.
#
#    Note
#    Many installations of sshd do not invoke your shell as the login shell when you directly run programs; what this means is that if your login shell is bash,
#    only .bashrc is read and not .bash_profile. As a workaround, make sure .bashrc sets up $PATH so that you can run git-receive-pack program.
#
#    Note
#    If you plan to publish this repository to be accessed over http, you should do mv my-git.git/hooks/post-update.sample my-git.git/hooks/post-update at this
#    point. This makes sure that every time you push into this repository, git update-server-info is run.
#
#Your "public repository" is now ready to accept your changes. Come back to the machine you have your private repository. From there, run this command:
#
#    $ git push <public-host>:/path/to/my-git.git master
#
#This synchronizes your public repository to match the named branch head (i.e. master in this case) and objects reachable from them in your current repository.
#
#As a real example, this is how I update my public Git repository. Kernel.org mirror network takes care of the propagation to other publicly visible machines:
#
#    $ git push master.kernel.org:/pub/scm/git/git.git/
#
#PACKING YOUR REPOSITORY
#Earlier, we saw that one file under .git/objects/??/ directory is stored for each Git object you create. This representation is efficient to create atomically and
#safely, but not so convenient to transport over the network. Since Git objects are immutable once they are created, there is a way to optimize the storage by
#"packing them together". The command
#
#    $ git repack
#
#will do it for you. If you followed the tutorial examples, you would have accumulated about 17 objects in .git/objects/??/ directories by now. git repack tells
#you how many objects it packed, and stores the packed file in .git/objects/pack directory.
#
#    Note
#    You will see two files, pack-*.pack and pack-*.idx, in .git/objects/pack directory. They are closely related to each other, and if you ever copy them by hand
#    to a different repository for whatever reason, you should make sure you copy them together. The former holds all the data from the objects in the pack, and
#    the latter holds the index for random access.
#
#If you are paranoid, running git verify-pack command would detect if you have a corrupt pack, but do not worry too much. Our programs are always perfect ;-).
#
#Once you have packed objects, you do not need to leave the unpacked objects that are contained in the pack file anymore.
#
#    $ git prune-packed
#
#would remove them for you.
#
#You can try running find .git/objects -type f before and after you run git prune-packed if you are curious. Also git count-objects would tell you how many
#unpacked objects are in your repository and how much space they are consuming.
#
#    Note
#    git pull is slightly cumbersome for HTTP transport, as a packed repository may contain relatively few objects in a relatively large pack. If you expect many
#    HTTP pulls from your public repository you might want to repack & prune often, or never.
#
#If you run git repack again at this point, it will say "Nothing new to pack.". Once you continue your development and accumulate the changes, running git repack
#again will create a new pack, that contains objects created since you packed your repository the last time. We recommend that you pack your project soon after the
#initial import (unless you are starting your project from scratch), and then run git repack every once in a while, depending on how active your project is.
#
#When a repository is synchronized via git push and git pull objects packed in the source repository are usually stored unpacked in the destination, unless rsync
#transport is used. While this allows you to use different packing strategies on both ends, it also means you may need to repack both repositories every once in a
#while.
#
#WORKING WITH OTHERS
#Although Git is a truly distributed system, it is often convenient to organize your project with an informal hierarchy of developers. Linux kernel development is
#run this way. There is a nice illustration (page 17, "Merges to Mainline") in Randy Dunlap's presentation[2].
#
#It should be stressed that this hierarchy is purely informal. There is nothing fundamental in Git that enforces the "chain of patch flow" this hierarchy implies.
#You do not have to pull from only one remote repository.
#
#A recommended workflow for a "project lead" goes like this:
#
# 1. Prepare your primary repository on your local machine. Your work is done there.
#
# 2. Prepare a public repository accessible to others.
#
#    If other people are pulling from your repository over dumb transport protocols (HTTP), you need to keep this repository dumb transport friendly. After git
#    init, $GIT_DIR/hooks/post-update.sample copied from the standard templates would contain a call to git update-server-info but you need to manually enable the
#    hook with mv post-update.sample post-update. This makes sure git update-server-info keeps the necessary files up-to-date.
#
# 3. Push into the public repository from your primary repository.
#
# 4. git repack the public repository. This establishes a big pack that contains the initial set of objects as the baseline, and possibly git prune if the
#    transport used for pulling from your repository supports packed repositories.
#
# 5. Keep working in your primary repository. Your changes include modifications of your own, patches you receive via e-mails, and merges resulting from pulling
#    the "public" repositories of your "subsystem maintainers".
#
#    You can repack this private repository whenever you feel like.
#
# 6. Push your changes to the public repository, and announce it to the public.
#
# 7. Every once in a while, git repack the public repository. Go back to step 5. and continue working.
#
#A recommended work cycle for a "subsystem maintainer" who works on that project and has an own "public repository" goes like this:
#
# 1. Prepare your work repository, by git clone the public repository of the "project lead". The URL used for the initial cloning is stored in the
#    remote.origin.url configuration variable.
#
# 2. Prepare a public repository accessible to others, just like the "project lead" person does.
#
# 3. Copy over the packed files from "project lead" public repository to your public repository, unless the "project lead" repository lives on the same machine as
#    yours. In the latter case, you can use objects/info/alternates file to point at the repository you are borrowing from.
#
# 4. Push into the public repository from your primary repository. Run git repack, and possibly git prune if the transport used for pulling from your repository
#    supports packed repositories.
#
# 5. Keep working in your primary repository. Your changes include modifications of your own, patches you receive via e-mails, and merges resulting from pulling
#    the "public" repositories of your "project lead" and possibly your "sub-subsystem maintainers".
#
#    You can repack this private repository whenever you feel like.
#
# 6. Push your changes to your public repository, and ask your "project lead" and possibly your "sub-subsystem maintainers" to pull from it.
#
# 7. Every once in a while, git repack the public repository. Go back to step 5. and continue working.
#
#A recommended work cycle for an "individual developer" who does not have a "public" repository is somewhat different. It goes like this:
#
# 1. Prepare your work repository, by git clone the public repository of the "project lead" (or a "subsystem maintainer", if you work on a subsystem). The URL used
#    for the initial cloning is stored in the remote.origin.url configuration variable.
#
# 2. Do your work in your repository on master branch.
#
# 3. Run git fetch origin from the public repository of your upstream every once in a while. This does only the first half of git pull but does not merge. The head
#    of the public repository is stored in .git/refs/remotes/origin/master.
#
# 4. Use git cherry origin to see which ones of your patches were accepted, and/or use git rebase origin to port your unmerged changes forward to the updated
#    upstream.
#
# 5. Use git format-patch origin to prepare patches for e-mail submission to your upstream and send it out. Go back to step 2. and continue.
#
#WORKING WITH OTHERS, SHARED REPOSITORY STYLE
#If you are coming from CVS background, the style of cooperation suggested in the previous section may be new to you. You do not have to worry. Git supports
#"shared public repository" style of cooperation you are probably more familiar with as well.
#
#See gitcvs-migration(7) for the details.
#
#BUNDLING YOUR WORK TOGETHER
#It is likely that you will be working on more than one thing at a time. It is easy to manage those more-or-less independent tasks using branches with Git.
#
#We have already seen how branches work previously, with "fun and work" example using two branches. The idea is the same if there are more than two branches. Let's
#say you started out from "master" head, and have some new code in the "master" branch, and two independent fixes in the "commit-fix" and "diff-fix" branches:
#
#    $ git show-branch
#    ! [commit-fix] Fix commit message normalization.
#     ! [diff-fix] Fix rename detection.
#      * [master] Release candidate #1
#    ---
#     +  [diff-fix] Fix rename detection.
#     +  [diff-fix~1] Better common substring algorithm.
#    +   [commit-fix] Fix commit message normalization.
#      * [master] Release candidate #1
#    ++* [diff-fix~2] Pretty-print messages.
#
#Both fixes are tested well, and at this point, you want to merge in both of them. You could merge in diff-fix first and then commit-fix next, like this:
#
#    $ git merge -m "Merge fix in diff-fix" diff-fix
#    $ git merge -m "Merge fix in commit-fix" commit-fix
#
#Which would result in:
#
#    $ git show-branch
#    ! [commit-fix] Fix commit message normalization.
#     ! [diff-fix] Fix rename detection.
#      * [master] Merge fix in commit-fix
#    ---
#      - [master] Merge fix in commit-fix
#    + * [commit-fix] Fix commit message normalization.
#      - [master~1] Merge fix in diff-fix
#     +* [diff-fix] Fix rename detection.
#     +* [diff-fix~1] Better common substring algorithm.
#      * [master~2] Release candidate #1
#    ++* [master~3] Pretty-print messages.
#
#However, there is no particular reason to merge in one branch first and the other next, when what you have are a set of truly independent changes (if the order
#mattered, then they are not independent by definition). You could instead merge those two branches into the current branch at once. First let's undo what we just
#did and start over. We would want to get the master branch before these two merges by resetting it to master~2:
#
#    $ git reset --hard master~2
#
#You can make sure git show-branch matches the state before those two git merge you just did. Then, instead of running two git merge commands in a row, you would
#merge these two branch heads (this is known as making an Octopus):
#
#    $ git merge commit-fix diff-fix
#    $ git show-branch
#    ! [commit-fix] Fix commit message normalization.
#     ! [diff-fix] Fix rename detection.
#      * [master] Octopus merge of branches 'diff-fix' and 'commit-fix'
#    ---
#      - [master] Octopus merge of branches 'diff-fix' and 'commit-fix'
#    + * [commit-fix] Fix commit message normalization.
#     +* [diff-fix] Fix rename detection.
#     +* [diff-fix~1] Better common substring algorithm.
#      * [master~1] Release candidate #1
#    ++* [master~2] Pretty-print messages.
#
#Note that you should not do Octopus because you can. An octopus is a valid thing to do and often makes it easier to view the commit history if you are merging
#more than two independent changes at the same time. However, if you have merge conflicts with any of the branches you are merging in and need to hand resolve,
#that is an indication that the development happened in those branches were not independent after all, and you should merge two at a time, documenting how you
#resolved the conflicts, and the reason why you preferred changes made in one side over the other. Otherwise it would make the project history harder to follow,
#not easier.
#SEE ALSO
#       gittutorial(7), gittutorial-2(7), gitcvs-migration(7), git-help(1), giteveryday(7), The Git User's Manual[1]

		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is 
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return git_trainer(
		'shutit.tk.git_trainer.git_trainer', 782914092.0001,
		description='',
		maintainer='',
		delivery_methods=['docker'],
		depends=['shutit.tk.setup']
	)

