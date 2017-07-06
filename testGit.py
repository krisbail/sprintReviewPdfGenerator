from git import Repo
import os
from os.path import expanduser


dest_dir = os.path.join(expanduser("~"), "sprintReview-data")
repo = None
if not os.path.exists(dest_dir):
    repo = Repo.clone_from("ssh://git@localhost:/var/git/sprintReview-data.git", dest_dir)
else:
    repo = Repo(dest_dir)


#repo = Repo.init("/tmp/testGit", mkdir=True, bare=False)
print repo.working_dir
print repo.working_tree_dir
print repo.untracked_files
print repo.index
print repo.is_dirty()
print repo.tags
print repo.tags[0].name if len(repo.tags) > 0 else "no tag"
print repo.head
print repo.branches
print repo.active_branch.name
print repo.remotes.origin
print repo.remotes.origin.refs.master
print repo.head.reference
print repo.head.commit
print repo.remotes.origin.refs.master.commit

origin = repo.remotes.origin
origin.fetch()

print origin.refs


master_commit = repo.heads.master.commit
origin_commit = repo.remotes.origin.refs.master.commit

repo.heads.master.checkout()
print master_commit.count()
print origin_commit.count()

if master_commit != origin_commit:
    if master_commit.count() > origin_commit.count():
        repo.remotes.origin.push()
    else:
        repo.remotes.origin.pull()
    pass

if "test" in origin.refs:

    #brancheTest_reference = repo.create_head("test", origin.refs.test)
    if "test" not in repo.branches:
        brancheTest_reference = repo.create_head("test")
        brancheTest_reference.set_tracking_branch(origin.refs.test)
        repo.remotes.origin.pull(origin.refs.test.remote_head)
    else:
        brancheTest_reference = repo.branches.test

    print brancheTest_reference.commit
    print origin.refs.test.commit
    print repo.head.reference.commit

    brancheTest_reference.checkout()


    if brancheTest_reference.commit != origin.refs.test.commit:
        print brancheTest_reference.commit
        print origin.refs.test.commit
        print repo.head.reference.commit

    pass






#repo.heads.coucou.checkout()


#if len(repo.untracked_files):
#    repo.index.add(repo.untracked_files)

if repo.is_dirty():
    #repo.index.commit("my first commit")
    #if repo.tag("26") is None:
     #   repo.create_tag("26", message="add sprint 26")
     pass


git = repo.git

if "retest" in repo.heads:
    repo.heads.retest.checkout()
    print "rebase"
    git.rebase("master")

#tagHead = repo.create_head('26') <<<<< create branch
#repo.head.reference = tagHead

#repo.head.reference = repo.tags[0]



#tag26 = repo.tag("26")
#repo.head.reference = tag26.reference
