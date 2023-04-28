import requests
from bs4 import BeautifulSoup


def _get_comments(URL):
    DATA = []

    page_contents = requests.get(URL).content

    soup = BeautifulSoup(page_contents, "html.parser")

    comments = soup.find_all("li", {"class": "top-level-reply"})

    if len(comments) == 0:
        return None

    for comment in comments:
        comment_id = comment.find("div", {"class": "comment"})['data-comment-id']
        user = comment.find("a", {"id": "comment-user"})['data-comment-user']
        content = str(comment.find("div", {"class": "content"}).text).strip()
        time = comment.find("span", {"class": "time"})['title']

        ALL_REPLIES = []
        replies = comment.find_all("li", {"class": "reply"})
        if len(replies) > 0:
            hasReplies = True
        else:
            hasReplies = False
        for reply in replies:
            r_comment_id = reply.find("div", {"class": "comment"})['data-comment-id']
            r_user = reply.find("a", {"id": "comment-user"})['data-comment-user']
            r_content = str(reply.find("div", {"class": "content"}).text).strip().replace("\n", "").replace(
                "                    ", " ")
            r_time = reply.find("span", {"class": "time"})['title']
            reply_data = {
                'CommentID': r_comment_id,
                'User': r_user,
                'Content': r_content,
                'Timestamp': r_time
            }
            ALL_REPLIES.append(reply_data)

        main_comment = {
            'CommentID': comment_id,
            'User': user,
            'Content': content,
            'Timestamp': time,
            'hasReplies?': hasReplies,
            'Replies': ALL_REPLIES
        }
        DATA.append(main_comment)
    return DATA


def get_user_comments(username, page=1):
    URL = f"https://scratch.mit.edu/site-api/comments/user/{username}/?page={page}"
    return _get_comments(URL=URL)


def get_studio_comments(studio_id, page=1):
    URL = f"https://scratch.mit.edu/site-api/comments/gallery/{studio_id}/?page={page}"
    return _get_comments(URL=URL)

def get_project_comments(project_id, page=1):
    URL = f"https://scratch.mit.edu/site-api/comments/project/{project_id}/?page={page}"
    return _get_comments(URL=URL)