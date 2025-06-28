import asyncio
import json

from fastmcp import Client
from google import genai
from google.genai import types
from cronjob import MyScheduler
from helper import add_comments, add_task_history, fetch_comments, fetch_post_url, fetch_url, get_media_id, set_media_id

instruction_list=[
    {"task_description":"Like interested users comment and send them link","task_id":"0",
    
     },{"task_id":"1","task_description":"bash/comeback negetive comments"},
    
]
GEMINI_API_KEY = "AIzaSyB5TK4d119fIweLsOjaoVChBV0cEEnVPSg"
googleai=genai.Client(api_key=GEMINI_API_KEY,)
MCP_SERVER_PATH = "./mcp_server.py"  # Path to your mcp_server.py

mcp_client = Client(MCP_SERVER_PATH)

myscheduler=MyScheduler()

async def analyze_comment_list(comment_list:list=[],post_caption:str=""):
    system_prompt=f"""Act as a social media manager who bashes negetive/roast type comments and dm the potential interested user.Based ont he below commentlist create a json tasklist for each user
     
       
       tasklist={instruction_list}
       Give response in below format:\n"""+"""
        [{"user_name":name of the user,"user_comment":"comment of the user","media_id":(str),"comment_id":"","task_list":[{task_id: , task_description}]}}]
"""
    result=googleai.models.generate_content(
                model='gemini-2.5-flash',contents=[types.Content(role="user",parts=[types.Part(text=f'comment list= {comment_list}')])],
        config=types.GenerateContentConfig(
                                                system_instruction=system_prompt,
                            temperature=0.7,
                            response_mime_type='application/json'
                            
                        ),)
    
    data=json.loads(result.candidates[0].content.parts[0].text)

    return data
    
async def get_bash_reply(user_reply:str):
    print("called baseh replyyyyyyyy")
    prompt="""based on user reply on my instagram post give a savage bashing reply in below json format:\n {"bash_reply":}"""
    result=await googleai.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Content(
        
        role="user",parts=[types.Part(text=f'user_reply:{user_reply}')])],config=types.GenerateContentConfig(
                                                system_instruction=prompt,
                            temperature=0.7,
                            response_mime_type='application/json'
                            
                        ))
    data=json.loads(result.candidates[0].content.parts[0].text)
    print(data)
    return data['bash_reply']
    
    

async def execute_tasks(tasklist:list=[]):
    if mcp_client is None:
        raise ValueError("mcp_client must be provided")
    print("started executing task")
    async with mcp_client as client:  # open once
        for i in tasklist:
            username = i['user_name']
            user_reply=i['user_comment']
            media_id=i['media_id']
            comment_id=i['comment_id']
            for j in i['task_list']:
                print("in tasklist--------")
                await asyncio.sleep(5)
                if j['task_id'] == "0":
                    
                    print(await client.call_tool(
                        name="send_message",
                        arguments={
                            "username": username,
                            "message": "Here's your link https://www.buy.com/xyz"
                        }
                    ))
                    add_task_history(f"Sent link to {username}")
                    print("Sent message to ",username)
                    
                elif(j['task_id'] == "1"):
                    bashing_reply=await get_bash_reply(user_reply=user_reply)
                    print(bashing_reply)
                    print(f"Bashing {username} for task {j['task_id']}{media_id} {int(comment_id) }")
                    await client.call_tool(
                        name=
                        "reply_to_comment",arguments={"media_id":media_id,"comment_id":int(comment_id),"reply_username":username,"text":bashing_reply})
                    add_task_history(f"Savage reply to a hater named  {username}")
                else:
                    print("no task",j['task_id'])

async def get_comments():

    
    media_id=get_media_id()['media_id']
    comments_list=[]
    async with mcp_client as client:
        
        comment_list=await client.call_tool(name="get_media_comments",arguments={
            "media_id": media_id, "amount": 10,
        })
        print(json.loads(comment_list[0].text))
        comment_list=json.loads(comment_list[0].text)
        add_comments(commentlist=comment_list['comments'])
    await mcp_client.close()
    data=fetch_comments()
    raw_comments=data['comments']
    print(raw_comments)
    comments_list=raw_comments
    
    comment_payload = [
{
    "text": c.text,
    "comment_id": c.pk,
    "media_id":media_id,
    "like_count": c.like_count or 0,
    "full_name": c.user.full_name or "",
    "username": c.user.username or ""
}
for c in comments_list
]
    print("baal=",comments_list)
    
    payload=await analyze_comment_list(comment_list=comment_payload,)
    print(payload)
    await execute_tasks(tasklist=payload)


async def get_post_data():
    async with mcp_client as client:
        
        postdata=await mcp_client.call_tool(name="get_post_info_from_url",arguments={"url":
                                                                                     f"{fetch_post_url()}"
                                                                                     })
        media_data_obj=json.loads(postdata[0].text)
        print(media_data_obj)
        print(type(media_data_obj['data']))
        id=media_data_obj['data']['id']
    
        print(f"media id=============={id}",)
        set_media_id(media_id=f"{id}")
       
        await get_comments()
        # print(json.loads(postdata[0].text))


# # asyncio.run(get_post_data())
# asyncio.run(get_comments())





    

