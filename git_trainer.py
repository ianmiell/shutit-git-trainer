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
		shutit.login('bash')
		shutit.send('rm -rf /tmp/shutit-git-trainer')
		shutit.send('mkdir -p /tmp/shutit-git-trainer')
		shutit.send('cd /tmp/shutit-git-trainer')

       and this will just output the name of the resulting tree, in this case (if you have done exactly as I’ve described) it should be

           8988da15d077d4829fc51d8544c097def6644dbb

       which is another incomprehensible object name. Again, if you want to, you can use git cat-file -t 8988d... to see that this time the object is not a "blob"
       object, but a "tree" object (you can also use git cat-file to actually output the raw object contents, but you’ll see mainly a binary mess, so that’s less
       interesting).

       However — normally you’d never use git write-tree on its own, because normally you always commit a tree into a commit object using the git commit-tree command. In
       fact, it’s easier to not actually use git write-tree on its own at all, but to just pass its result in as an argument to git commit-tree.

       git commit-tree normally takes several arguments — it wants to know what the parent of a commit was, but since this is the first commit ever in this new
       repository, and it has no parents, we only need to pass in the object name of the tree. However, git commit-tree also wants to get a commit message on its
       standard input, and it will write out the resulting object name for the commit to its standard output.

       And this is where we create the .git/refs/heads/master file which is pointed at by HEAD. This file is supposed to contain the reference to the top-of-tree of the
       master branch, and since that’s exactly what git commit-tree spits out, we can do this all with a sequence of simple shell commands:

           $ tree=$(git write-tree)
           $ commit=$(echo 'Initial commit' | git commit-tree $tree)
           $ git update-ref HEAD $commit

       In this case this creates a totally new commit that is not related to anything else. Normally you do this only once for a project ever, and all later commits will
       be parented on top of an earlier commit.

       Again, normally you’d never actually do this by hand. There is a helpful script called git commit that will do all of this for you. So you could have just written
       git commit instead, and it would have done the above magic scripting for you.

MAKING A CHANGE
       Remember how we did the git update-index on file hello and then we changed hello afterward, and could compare the new state of hello with the state we saved in
       the index file?

       Further, remember how I said that git write-tree writes the contents of the index file to the tree, and thus what we just committed was in fact the original
       contents of the file hello, not the new ones. We did that on purpose, to show the difference between the index state, and the state in the working tree, and how
       they don’t have to match, even when we commit things.

       As before, if we do git diff-files -p in our git-tutorial project, we’ll still see the same difference we saw last time: the index file hasn’t changed by the act
       of committing anything. However, now that we have committed something, we can also learn to use a new command: git diff-index.

       Unlike git diff-files, which showed the difference between the index file and the working tree, git diff-index shows the differences between a committed tree and
       either the index file or the working tree. In other words, git diff-index wants a tree to be diffed against, and before we did the commit, we couldn’t do that,


		shutit.logout()
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
		delivery_methods=['bash'],
		depends=['shutit.tk.setup']
	)

