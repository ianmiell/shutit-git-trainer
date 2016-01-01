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
		shutit.send('git config --global user.email "you@utopia.com"')
		shutit.send('git config --global user.name "NoName"')
		shutit.send('mkdir git-tutorial && cd git-tutorial',note='Make a directory for our first repository and move into it.')
		shutit.send('git init',note='Initialise our git repository')
		shutit.send('ls .git',note='A .git directory has been created, with a file HEAD and two directories (objects and refs).\n\nThe file called head is similar to a symboilc link and points to refs/heads/master (which does not exist yet).\n\nobjects contains the real data of your project, and refs contains references to these data.\n\nThe special master head is the default branch, which is why the .git/HEAD file was created points to it even if it does not yet exist. Basically, the HEAD link is supposed to always point to the branch you are working on right now, and you always start out expecting to work on the master branch. An advanced user may want to take a look at gitrepository-layout(5) after finishing this tutorial.')
		shutit.send('ls .git/refs',note='refs contains references to any number of different heads of development (branches) and to any tags for specific versions you create.')

		# POPULATING A GIT REPOSITORY
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

		# COMMITTING GIT STATE
		tree_id = shutit.send_and_get_output('git write-tree',note='Take the files in the index, and commit them as a so-called tree. It will output the name of the resulting tree.')
		shutit.send('git cat-file -t ' + tree_id,note='This time the object created is not a blob, but a tree object.')
		shutit.send('git cat-file tree ' + tree_id,note='This time the output of the file is less comprehensible.')
		shutit.send('tree=$(git write-tree)',note='We will do that again, but store the tree id in an environment variable.')
		shutit.send('commit=$(echo commit | git commit-tree $tree)',note='Now use the commit-tree command, which normally takes three arguments: the parent commit id (not required here as there is no parent), the tree id we just created, and commit message, which we pipe in.')
		shutit.send('git update-ref HEAD $commit',note='Now we tell git that the HEAD of the tree should point to the commit we just made.')
		shutit.send('git commit',note='The above three commands can be shortened to "git commit".')

		# MAKING A CHANGE
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
		shutit.send('git tag my-first-tag',note='A tag is basically the same as a branch, but we put it in the .git/refs/tags subdirectory instead of calling it a head.\n\nYou can diff against it (and so on) just as you would a branch.')
		shutit.send('ls .git/refs/tags',note='The list of tags is stored here.')
		shutit.send('git tag -s my-second-tag -m "a message" HEAD',note='You can create annotated tags with a -s or -a flag. HEAD could be changed to another branch if desired.')

		# CREATING A NEW BRANCH
		shutit.send('git checkout -b mybranch',note='Creates a branch based at the current HEAD, and switches to it. Branches in Git are really nothing more than pointers into the Git object database from within the .git/refs/ subdirectory, and as we already discussed, the HEAD branch is nothing but a symlink to one of these object pointers.')
		shutit.send('ls .git/refs/heads',note='The branches are stored here')
		shutit.send('git checkout master',note='')
		shutit.send('cat .git/HEAD',note='Where are we pointed at now?')
		shutit.send('git branch',note='List the branches we have')
		shutit.send('git branch another_branch',note='Create a branch but do not switch to it.')

		# MERGING TWO BRANCHES
		shutit.send('git checkout mybranch',note='Get back on to the branch you just created.')
		shutit.send('echo "Work, work, work" >> hello',note='Do some work')
		shutit.send('git commit -m "Some work." -i hello',note='git commit by just giving the filename directly to git commit, with an -i flag (which tells Git to include that file in addition to what you have done to the index file so far when making the commit).')
		shutit.send('git checkout master',note='''Now, to make it a bit more interesting, let's assume that somebody else does some work in the original branch, and simulate that by going back to the master''')
		shutit.send('''echo "Play, play, play" >> hello''',note='Add some work to master')
		shutit.send('''echo "Lots of fun" >> example''',note='And some more work')
		shutit.send('''git commit -m "Some fun." -i hello example''',note='Commit that work to the master branch.')
		shutit.send('git merge -m "Merge work in mybranch" mybranch',note='Merge in the work done on mybranch, and put it into the master branch. This causes a conflict which you could resolve here if you want, but this will be done for you.')
		shutit.send('''cat > hello << END
Hello World
It's a new day for git
Play, play, play
Work, work, work
END''')
		shutit.send('git commit -i -m "hello merged" hello',note='Commit the merge')
		shutit.send('git show-branch --topo-order --more=1 master mybranch',note='''Another useful tool, especially if you do not always work in X-Window environment, is git show-branch.

    $ git show-branch --topo-order --more=1 master mybranch
    * [master] Merge work in mybranch
     ! [mybranch] Some work.
    --
    -  [master] Merge work in mybranch
    *+ [mybranch] Some work.
    *  [master^] Some fun.

The first two lines indicate that it is showing the two branches with the titles of their top-of-the-tree commits, you are currently on master branch (notice the
asterisk * character), and the first column for the later output lines is used to show commits contained in the master branch, and the second column for the
mybranch branch. Three commits are shown along with their titles. All of them have non blank characters in the first column (* shows an ordinary commit on the
current branch, - is a merge commit), which means they are now part of the master branch. Only the "Some work" commit has the plus + character in the second
column, because mybranch has not been merged to incorporate these commits from the master branch. The string inside brackets before the commit log message is a
short name you can use to name the commit. In the above example, master and mybranch are branch heads. master^ is the first parent of master branch head. Please
see gitrevisions(7) if you want to see more complex cases.

    Note
    Without the --more=1 option, git show-branch would not output the [master^] commit, as [mybranch] commit is a common ancestor of both master and mybranch
    tips. Please see git-show-branch(1) for details.

    Note
    If there were more commits on the master branch after the merge, the merge commit itself would not be shown by git show-branch by default. You would need to
    provide --sparse option to make the merge commit visible in this case.
''')
		shutit.send('git checkout mybranch', note='Now, say are the one who did all the work in mybranch, and the fruit of your hard work has finally been merged to the master branch.')
		shutit.send('git merge -m "Merge upstream changes." master',note='Run git merge to get the so-called "upstream changes" back to your "downstream" branch.')

		shutit.send('git show-branch master mybranch',note='Because your branch did not contain anything more than what had already been merged into the master branch, the merge operation did not actually do a merge. Instead, it just updated the top of the tree of your branch to that of the master branch. This is often called fast-forward merge. You can run show-branch, which tells you this.')
		#TODO
		# COPYING REPOSITORIES - TODO
#    $ git clone rsync://rsync.kernel.org/pub/scm/git/git.git/ my-git
#    $ cd my-git
#    $ git checkout
#
#which will end up doing all of the above for you.
#
#You have now successfully copied somebody else's (mine) remote repository, and checked it out.
		# MERGING EXTERNAL WORK
		# HOW DOES THE MERGE WORK?
		# PUBLISHING YOUR WORK
		# PACKING YOUR REPOSITORY
		# WORKING WITH OTHERS
		# WORKING WITH OTHERS, SHARED REPOSITORY STYLE
		# BUNDLING YOUR WORK TOGETHER
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

