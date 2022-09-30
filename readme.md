# API service for Yatube web service

<p align="right">
<a href="https://docs.python.org/3.9/">
<img src="https://img.shields.io/badge/Python-3.9-FFE873.svg?
labelColor=4B8BBE" 
alt="Python requirement">
</a>
</p>

## About

API service for interaction with `posts` Django application using
[JSON](https://www.json.org/json-en.html) encoding.

Tech stack: \
[FastAPI],
[SQLAlchemy]

## Endpoints

**posts**

attributes:\
`post_id`: integer

* `api/v1/api-token-auth/` (POST): passes login/password and gets
  Authentication token
* `api/v1/posts/` (GET, POST): gets list of all posts or creates new post
* `api/v1/posts/{post_id}/` (GET, PUT, PATCH, DELETE): gets, modifies or 
  deletes a post by its `id`

**groups**

attributes:\
`group_id`: integer

* `api/v1/groups/` (GET): gets list of all groups
* `api/v1/groups/{group_id}/` (GET): gets a post by its `id`

**comments**

attributes:\
`post_id`: integer\
`comment_id`: integer

* `api/v1/posts/{post_id}/comments/` (GET, POST): gets list of all comments 
  for a post with `id=post_id` or creates new comment for the post
* `api/v1/posts/{post_id}/comments/{comment_id}/` (GET, PUT, PATCH, DELETE):
  gets, modifies or deletes a comment by its `id` for a post with `id=post_id`
