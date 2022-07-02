import re
import os

SB_PICS = 'SB_PICS'
SB_POSTS = 'SB_POSTS'
SB_FILE = 'Shine BDSM_ записи сообщества _ ВКонтакте256.html'
SB_FILE = 'Shine BDSM _ ВКонтакте.html'

TPL_PAGE = """<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
	<link rel="stylesheet" href="main.css">
</head>
<body>
	
%s

</body>
</html>"""

TPL_POST = """<div class="post">
        <p><div class="post-header">%s - %s</div></p>
	<div class="post-text">
	<img src="%s" width="400" class="leftimg">
	%s
	</div>
</div>"""

def gen_txt():
    with open(SB_FILE) as fh:
        html_text = fh.read()
        regex = re.compile(r'<div class="post_content">(.*?)</div></div></div>', re.DOTALL)
        res = re.findall(regex, html_text)

        i = 1
        for post in res:
            with open('SB_POSTS/%s.txt'%i,'w') as fh2:
                fh2.write(post)
            i += 1

def parse_post(post_text):
    post = {}

    try:
        regex = re.compile(r'</a>[ ]{0,1}<br>(.*?)</div><div class', re.DOTALL)
        res = re.findall(regex, post_text)        
        post['text'] = res[0]
    except IndexError:
        try:
            regex = re.compile(r'wall_post_text">(.*?)</div><div class', re.DOTALL)
            res = re.findall(regex, post_text)
            post['text'] = res[0]
        except IndexError:
            try:
                regex = re.compile(r'</a>[ ]{0,1}<br>(.*?)</span>', re.DOTALL)
                res = re.findall(regex, post_text)        
                post['text'] = res[0]
            except IndexError:
                ##print(post_text)
                raise IndexError
        

    post['text'] = re.sub('<a class="wall_post_more".*?display: none">', '', post['text'])
    
    regex = re.compile(r'\/(.*?)[?]size', re.DOTALL)
    res = re.findall(regex, post_text)
    if len(res) > 0:
        pic = res[-1].split('/')[-1]
    else:
        pic = None
    post['pic'] = pic

    return post

def read_txt(sb_posts):
    posts = []
    postdir_fullpath = os.path.join(os.getcwd(), sb_posts)
    for item in os.listdir(postdir_fullpath):
        print(item)
        post_fullpath = os.path.join(postdir_fullpath, item)
        with open(post_fullpath) as fh:
            post_text = fh.read()
            post_info = parse_post(post_text)
            post_info['file'] = item

            if post_info['pic']:
                old_picname = post_info['pic']
                post_num = post_info['file'].split('.')[0]
                post_pic = old_picname.split('.')[0]
                if post_num != post_pic:
                    old_picpath = os.path.join(SB_PICS, old_picname)
                    new_picpath = os.path.join(SB_PICS, old_picname.replace(post_pic, post_num))

                    if os.path.exists(old_picpath) and os.path.isfile(old_picpath):
                        os.rename(old_picpath, new_picpath)
    
                post_info['pic'] = old_picname.replace(post_pic, post_num)
                
                
            posts.append(post_info)
    return posts


def gen_html(posts):
    text = []
    for post in posts:
        if post['pic']:
            text.append(TPL_POST % (post['file'], str(post['pic']), SB_PICS + '/' + str(post['pic']), post['text']))

    html = TPL_PAGE % ''.join(text)

    with open('sb2.html', 'w', encoding='utf-8') as fh:
        fh.write(html)
        
#gen_txt()
gen_html(read_txt(SB_POSTS))













