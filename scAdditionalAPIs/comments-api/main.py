from API import *
from fastapi import FastAPI

description = "Simple API to get the comments of a Scratch User, Studio and Project in JSON format!"

tags_metadata = [
    {
        "name": "root",
        "description": "Root Page.",
    },
    {
        "name": "user",
        "description": "Get the comments of a Scratch User.",
    },
    {
        "name": "studio",
        "description": "Get the comments of a Scratch Studio.",
    },
    {
        "name": "project",
        "description": "Get the comments of a Scratch Project.",
    },
]

app = FastAPI(
    title="Scratch Comments API",
    description=description,
    version="1.0",
    docs_url="/docs",
    openapi_tags=tags_metadata
)


@app.get("/", tags=["root"])
async def root():
    return {"Name": "Scratch Comments API", "Version": "1.0",
            "Description": "API to get the comment data of a Scratch User, Studio, Project in JSON format",
            "Documentation": "Go to /docs endpoint", "Made by": "Sid72020123"}


@app.get("/user/", tags=["user"])
async def user(username: str, limit: int = 5, page: int = 1):
    data = []
    try:
        comment_data = get_user_comments(username=username, page=page)
        if comment_data is None:
            return {"Error": True, "Info": "User Not Found or has no comments"}
        l = 0
        p = page
        while l < limit:
            try:
                comment = comment_data[l]
                data.append(comment)
            except IndexError:
                p += 1
                comment_data = get_user_comments(username=username, page=p)
                if comment_data is None:
                    break
            l += 1
    except:
        return {"Error": True, "Message": "An Error Occurred!"}
    return data


@app.get("/studio/", tags=["studio"])
async def studio(id: int, limit: int = 5, page: int = 1):
    data = []
    try:
        comment_data = get_studio_comments(studio_id=id, page=page)
        if comment_data is None:
            return {"Error": True, "Info": "Studio Not Found or has no comments"}
        l = 0
        p = page
        while l < limit:
            try:
                comment = comment_data[l]
                data.append(comment)
            except IndexError:
                p += 1
                comment_data = get_studio_comments(studio_id=id, page=page)
                if comment_data is None:
                    break
            l += 1
    except:
        return {"Error": True, "Message": "An Error Occurred!"}
    return data


@app.get("/project/", tags=["project"])
async def project(id: int, limit: int = 5, page: int = 1):
    data = []
    try:
        comment_data = get_project_comments(project_id=id, page=page)
        if comment_data is None:
            return {"Error": True, "Info": "Project Not Found or has no comments"}
        l = 0
        p = page
        while l < limit:
            try:
                comment = comment_data[l]
                data.append(comment)
            except IndexError:
                p += 1
                comment_data = get_project_comments(project_id=id, page=page)
                if comment_data is None:
                    break
            l += 1
    except:
        return {"Error": True, "Message": "An Error Occurred!"}
    return data