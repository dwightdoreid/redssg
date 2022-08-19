from datetime import datetime
from bs4 import BeautifulSoup
import jinja2, os, json, time, shutil


def copyFile(path1, path2):
    f = open(path1, 'r')
    f2 = open(path2, "w")
    f2.write(f.read())
    f.close()
    f2.close()


def getDate(e):
    dt_string = e["date_published"]
    format = "%B %d, %Y"
    dt_obj = datetime.strptime(dt_string, format)
    t = time.mktime(dt_obj.timetuple())
    return t

##################################################################################################################
###Create output directory
parent_dir = os.getcwd()
dir = "site"
path = os.path.join(parent_dir, dir)
if not os.path.exists(path):
    os.mkdir(path)
########################################################################################
###Read Posts Data
########################################################################################
posts_meta = []
posts_titles = list()
for root, dirs, files in os.walk("posts", topdown=False):
    for name in dirs:
        posts_titles.append(name)
########################################################################################
###Create Post Directories
########################################################################################
parent_dir = os.getcwd()
for title in posts_titles:
    dir = title.casefold().replace(" ", "-")
    path = os.path.join(parent_dir, "site", dir)
    if not os.path.exists(path):
        os.mkdir(path)
########################################################################################
###Copy Images from Posts Folders to Site Folders
########################################################################################
indx = 0
for dir in posts_titles:
    site_dir = posts_titles[indx].casefold().replace(" ", "-")
    site_path = os.path.join(parent_dir, "site", site_dir)
    path = os.path.join("posts", dir)
    with os.scandir(path) as post_dirs:
        for file in post_dirs:
            if file.name.endswith('.png'):
                # print(file.name)
                shutil.copy2(file.path, site_path+"/"+file.name)
    indx+=1
########################################################################################        
###Create Site Home Index File
######################################################################################## 
templateLoader = jinja2.FileSystemLoader(searchpath="./")
env = jinja2.Environment(loader=templateLoader)
header_template = env.get_template('header.html')
header = header_template.render(title="dwightreid.com", home_link = "/site", description="Hey, my site is about general scientific modeling and simulation with a lot of content on power systems and energy technology. Read on.")

footer_template = env.get_template('footer.html')
footer = footer_template.render(home_link = "/site",year="2022")

for title in posts_titles:
    f = open(os.path.join("posts", title, "post-meta.json"), 'r')
    x = f.read()
    y = json.loads(x)
    y["link"] = "/site/"+title.casefold().replace(" ", "-")
    x = json.dumps(y)
    posts_meta.append(json.loads(x))
    f.close()

posts_meta.sort(reverse=True, key=getDate)

context = {
        "title": "Results",
        "posts": posts_meta,
        "test_name": "test_name",
        "max_score": 100,
    }
# print(type(context))
home_template = env.get_template('home.html')
home = home_template.render(**context)

doc = header + home + footer

f = open("site/index.html", "w")
f.write(doc)
f.close()

copyFile("style.css", "site/style.css")
########################################################################################        
###Create Posts Home Index Files
######################################################################################## 
indx = 0
title = posts_titles[indx]

for title in posts_titles:
    f = open(os.path.join("posts", title, "post-meta.json"), 'r')
    x = f.read()
    y = json.loads(x)
    # print(y["snippet"][0])
    header = header_template.render(title="dwightreid.com", home_link = "/site", description=y["snippet"][0])

    site_dir = title.casefold().replace(" ", "-")
    site_path = os.path.join(parent_dir, "site", site_dir)
    shutil.copy2("style.css", site_path+"/style.css")

    dir = title
    f = open(os.path.join("posts", dir, "index.html"), 'r')
    x = f.read()
    html_doc = BeautifulSoup(x, 'html.parser')
    html_doc_body = str(html_doc.body)
    f.close()

    doc = header + html_doc_body + footer
    post_path = os.path.join(parent_dir, "site", site_dir, "index.html")
    f = open(post_path, "w")
    f.write(doc)
    f.close()