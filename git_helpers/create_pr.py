from utils.sh import sh

def create_commit_message(title, source_branch_name, target_branch_name, id_str, reviewers_str, assignees_str):
    commit_message = ''

    if title is not None:
        commit_message = title
    else:
        commit_message = source_branch_name + '<-' + target_branch_name
    
    if id_str is not None:
        commit_message = '[#' + id_str + ']' + commit_message
    
    commit_message += '\n'

    if id_str is not None:
        commit_message += '\n' + 'Closes #' + id_str
        commit_message += '\n' + 'Fixes #' + id_str
        commit_message += '\n' + 'Resolves #' + id_str

    if reviewers_str is not None:
        reviewers = reviewers_str.split(',')
        
        if len(reviewers) > 0:
            commit_message += '\nReviewer'

            if len(reviewers) > 1:
                commit_message += 's'
            
            commit_message += ':'
        
        for reviewer in reviewers:
            commit_message += ' @' + reviewer
    
    if assignees_str is not None:
        assignees = assignees_str.split(',')
        
        if len(assignees) > 0:
            commit_message += '\nAssignee'

            if len(reviewers) > 1:
                commit_message += 's'
            
            commit_message += ':'
        
        for assignee in assignees:
            commit_message += ' @' + assignee
    
    return commit_message

source_branch_name = sh('git rev-parse --abbrev-ref HEAD')
target_branch_name = 'develop'

input('\n\nWill create pull request\n\'' + target_branch_name + '\' <- \'' + source_branch_name + '\'\nPress Enter to proceed ')

label = None
if '/' in source_branch_name:
    label = source_branch_name.split('/')[0]

id_str = None
if '-' in source_branch_name.split('/')[-1]:
    id_str = source_branch_name.split('-')[-1]

title = input('\n\nEnter a title for the PR, or leave empty if None\nPress Enter to afterwards\nTITLE: ')
if len(title) == 0:
    title = None

reviewers_str = input('\n\nEnter name of REVIEWERS (comma separated string, no spaces), leave empty if None\nEX: \'user1,user2\'\nPress Enter to afterwards\nREVIEWERS: ')
if len(reviewers_str) == 0:
    reviewers_str = None

assignees_str = input('\n\nEnter name of ASSIGNEES (comma separated string, no spaces), leave empty if None\nEX: \'user1,user2\'\nPress Enter to afterwards\nASSIGNEES: ')
if len(assignees_str) == 0:
    assignees_str = None

commit_message = create_commit_message(title, source_branch_name, target_branch_name, id_str, reviewers_str, assignees_str)
cmd = "hub pull-request -m $'" + commit_message + "'"

if id_str is not None:
    cmd += ' -i ' + id_str

cmd += ' -o'

if reviewers_str is not None:
    cmd += ' -r ' + reviewers_str

if assignees_str is not None:
    cmd += ' -a ' + assignees_str

if label is not None:
    cmd += ' -l ' + label

print(sh(cmd))