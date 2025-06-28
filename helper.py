import json
from pathlib import Path
from venv import logger
from instagrapi.types import Comment

json_file = Path("C:/aiprojects/instagram_dm_mcp/src/exa_helper/anniedb.json")

def set_post_url(post_url:str):
    # Load existing data or create default if file doesn't exist
    if json_file.exists():
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    # Set the task_id
    data["post_url"] = post_url



    # Write back to file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Post url set '{post_url}'")


def set_task(task_id="task1"):
    # Load existing data or create default if file doesn't exist
    if json_file.exists():
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    # Set the task_id
    data["task_id"] = task_id



    # Write back to file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Task set to '{task_id}'")


def do_task_exist():

    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return False
   
    return bool(data.get("task_id", "").strip())
def fetch_post_url():
    with open(json_file,'r',encoding='utf-8') as f:
        content=f.read().strip()
        data=json.loads(content)
    print(data)
    dm_url=data.get("post_url","https://www.instagram.com/p/DLbzn4VzrMu/")
    return dm_url
def fetch_url():
    with open(json_file,'r',encoding='utf-8') as f:
        content=f.read().strip()
        data=json.loads(content)
    print(data)
    dm_url=data.get("dm_url","https://www.instagram.com/p/DLbzn4VzrMu/")
    return dm_url
def fetch_comments() -> dict:
    """
    Fetch comment_list from anniedb.json and return as list of Comment objects.

    Returns:
        dict: {
            success: bool,
            comments: list[Comment] (if any),
            message: str,
            error: str (if any)
        }
    """
    try:
        # Check file existence
        if not json_file.exists():
            return {
                "success": False,
                "comments": [],
                "message": f"{json_file} not found.",
                "error": "FileNotFound"
            }

        # Load and parse JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {
                    "success": True,
                    "comments": [],
                    "message": "File is empty",
                    "error": None
                }
            data = json.loads(content)

        raw_comments = data.get("comment_list", [])
        comments = [Comment(**c) for c in raw_comments]

        return {
            "success": True,
            "comments": comments,
            "message": f"{len(comments)} comments fetched.",
            "error": None
        }

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return {
            "success": False,
            "comments": [],
            "message": "JSON decode error",
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "comments": [],
            "message": "Unexpected error",
            "error": str(e)
        }

def add_comments(commentlist: list[Comment] = []) -> dict:
    """
    Add comments to anniedb.json under 'comment_list'.

    Args:
        commentlist (list[Comment]): List of Comment objects to add.

    Returns:
        dict: {
            success: bool,
            message: str,
            error: str (if any)
        }
    """
    try:
        # Step 1: Load or initialize data
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                data = json.loads(content) if content else {}
        else:
            data = {}

        # Step 2: Get existing comments or initialize
        existing_comments = data.get("comment_list", [])

        # Step 3: Convert Comment objects to dicts and append
        new_comments = [comment for comment in commentlist]
        existing_comments.extend(new_comments)

        # Optional: De-duplicate by comment pk (if needed)
        unique_comments = {c['pk']: c for c in existing_comments}.values()

        # Step 4: Update and save
        data["comment_list"] = list(unique_comments)

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Added {len(new_comments)} comments to anniedb.json")
        return {
            "success": True,
            "message": f"{len(new_comments)} comments added",
            "error": None
        }

    except Exception as e:
        logger.error(f"Error adding comments: {str(e)}")
        return {
            "success": False,
            "message": "Failed to add comments",
            "error": str(e)
        }



def set_media_id(media_id: str) -> dict:
    """
    Sets the media_id field in anniedb.json, preserving other fields.

    Args:
        media_id: Instagram media ID to set.

    Returns:
        dict: {
            success: bool,
            message: str,
            error: str (if any)
        }
    """
    try:
        if not isinstance(media_id, str) or not media_id.strip():
            return {
                "success": False,
                "message": "Invalid media_id: must be a non-empty string",
                "error": "Invalid input"
            }

        # Load existing or fallback to defaults
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                data = json.loads(content) 
        else:
            return 

        if data.get("media_id") == media_id:
            return {
                "success": True,
                "message": f"Media ID already set to {media_id}",
                "error": None
            }

        # Update media_id only
        data["media_id"] = media_id

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Media ID set to {media_id}")
        return {
            "success": True,
            "message": f"Media ID updated to {media_id}",
            "error": None
        }

    except Exception as e:
        logger.error(f"Failed to set media_id: {str(e)}")
        return {
            "success": False,
            "message": "Failed to set media_id",
            "error": str(e)
        }
def get_media_id() -> dict:
    """
    Load anniedb.json and return the current media_id.

    Returns:
        dict: {
            success: bool,
            media_id: str (if found),
            message: str,
            error: str (if any)
        }
    """
    try:
        if not json_file.exists():
            return {
                "success": False,
                "media_id": None,
                "message": f"{json_file} does not exist",
                "error": "FileNotFound"
            }

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        media_id = data.get("media_id", "")
        if not media_id:
            return {
                "success": False,
                "media_id": None,
                "message": "media_id is not set",
                "error": "EmptyMediaID"
            }

        return {
            "success": True,
            "media_id": media_id,
            "message": "media_id retrieved successfully",
            "error": None
        }

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse {json_file}: {str(e)}")
        return {
            "success": False,
            "media_id": None,
            "message": "Failed to parse JSON file",
            "error": str(e)
        }
    except IOError as e:
        logger.error(f"File error with {json_file}: {str(e)}")
        return {
            "success": False,
            "media_id": None,
            "message": "File read error",
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_media_id: {str(e)}")
        return {
            "success": False,
            "media_id": None,
            "message": "Unexpected error",
            "error": str(e)
        }



def add_task_history(message:str=""):
    with open(json_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

        data = json.loads(content)
        
        data['task_history'].append(message)
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
def get_task_history():
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()

            data = json.loads(content)
        return data['task_history']


def reset_task():
    with open(json_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

        data = json.loads(content)
        
        data=    {
  "media_id": "",
  "post_url": "",
  "task_id":"",
  "dm_url":"",
  "sent_reply_username": [],
  "bashed_reply_username": [],
  "comment_list": [
   
  ]
  ,"task_history":[]
}
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
