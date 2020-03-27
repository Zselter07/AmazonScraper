from bs4 import BeautifulSoup as bs

import os, requests

def sh(command):
    stream = os.popen(command)

    return stream.read().strip('\n').strip(' ')

def project_name_to_id(name):
    project_id = ''
    should_add = True
    separators = [
        '-', ' ', '_'
    ]

    for c in name:
        s = str(c)

        if (should_add or s == s.upper()) and s not in separators:
            project_id += s
        
        if s in separators:
            should_add = True
        else:
            should_add = False
    
    if len(project_id) == 0:
        project_id = name
    
    return project_id

def read_url():
    while True:
        url = input('\n\nEnter issue URL and press ENTER\nEx: \'https://github.com/Zselter07/AmazonScraper/issues/5\'\n')

        if '/issues/' in url and 'github.com/' in url:
            break
        else:
            print('Wrong URL')
    
    return url

def preformat_url(url):
    if 'https://' not in url:
        url = 'https://' + url

    if 'www.github.com' in url:
        url = url.replace('www.github.com', 'github.com')
    
    return url

def get_issue_properties_from_url(url):
    comps = issue_url.replace('https://github.com/', '').split('/')
    
    return comps[1], int(comps[3])

def get_issue_properties(issue_url):
    try:
        resp = requests.get(issue_url)

        if resp is None:
            return None

        if resp.status_code != 200:
            return None
        
        soup = bs(resp.content, 'html.parser')
        title = soup.find('title').encode_contents().decode('utf-8').split('·')[0].strip()
        description = ''

        try:
            description = soup.find('meta', attrs={'name':'description'})['content'].strip()
        except:
            pass

        if description == '':
            description = None
        
        label = None
        try:
            label = soup.find('a', class_='sidebar-labels-style box-shadow-none width-full d-block IssueLabel')['data-name']
        except Exception as e:
            print(e)
        
        return title, description, label
    except Exception as e:
        print('ERROR:', e)

        return None, None, None

def create_commit_message(title, description, issue_url, issue_num, branch_name):
    commit_message = '[#' + str(issue_num) + '] - ' + title + '\n'

    if description is not None:
        commit_message += '\n' + 'Description: ' + description + '\n'

    commit_message += '\n' + 'Closes #' + str(issue_num)
    commit_message += '\n' + 'Message: Created branch named \'' + branch_name + '\''

    return commit_message

def push_branch(commit_message, branch_name):
    print('\n\n\n' + commit_message + '\n\n\n')
    print(sh('git config credential.helper store'))
    print(sh('git reset HEAD .'))
    print(sh('git checkout develop'))
    print(sh('git pull'))
    print(sh('git checkout -b ' + branch_name))
    print(sh('git checkout ' + branch_name))
    print(sh("git commit --allow-empty -m $'" + commit_message + "'"))
    print(sh('git push -u origin ' + branch_name))
    print(sh('git fetch'))

issue_url = preformat_url(read_url())
board_name, issue_num = get_issue_properties_from_url(issue_url)
branch_name = project_name_to_id(board_name) + '-' + str(issue_num)

title, description, label = get_issue_properties(issue_url)

if label is not None:
    label = label.replace(' ', '-')

if title is None:
    print('Something went wrong. Issue title is None and it shouldn\'t be. Exiting.')
    exit(0)

if label is not None:
    branch_name = label + '/' + branch_name

user_defined_branch_name = input('\n\nSuggested branch name\n<' + branch_name + '>\nType new one to override, leave empty to use it. Press Enter, when finished\n')

if len(user_defined_branch_name) > 0:
    branch_name = user_defined_branch_name

commit_message = create_commit_message(title, description, issue_url, issue_num, branch_name)
push_branch(commit_message, branch_name)