
print("Starting...")

import os,asyncio,uvloop,importlib,sys,re,traceback

uvloop.install()


from home import *


@handler(pattern="/bash(?: |$)(.*)",admin=True)
async def event(event): 
 ss = await event.reply(f'`Processing...`')
 try:
    loop = asyncio.get_event_loop()
    tname = (asyncio.current_task()).get_name()
    te = f"Type `/ctask {tname}` to Stop"
    cmd = event.pattern_match.group(1).strip()    
    if not cmd:
        await ss.edit("`[Error] Give me a command`")
        return
    ss = await ss.edit(f'`Running Terminal.....`\n\n{te}')
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    text = f"**Terminal Command**: `{cmd}`\n**Return code**: `{process.returncode}`\n\n"
    if stdout:      
        text += "\n**[stdout]**\n`" + stdout.decode("UTF-8").strip() + "`\n"
    if stderr:
        text += "\n**[stderr]**\n`" + stderr.decode('UTF-8').strip() + "`\n"   
    if len(text) > 4096:               
       output = open("term.txt", "w+")
       output.write(text)
       output.close()
       await event.reply(file="term.txt")
       return os.remove("term.txt")           
    else:
      return await ss.edit(text)  
 except asyncio.CancelledError:
    return await ss.edit("`Terminal Stopped`")


import importlib.util

@handler(pattern="/install(?: |$)(.*)",admin=True)
async def install(event):
    ss = await event.reply("`Installing....`")
    xi = 'Installed'
    if event.reply_to_msg_id:
            imodule = await event.client.download_media(await event.get_reply_message())    
            cr = (os.path.splitext(os.path.basename(imodule))[0])
            if cr in cmd.keys(): 
               for i in cmd[cr]: 
                   tbot.remove_event_handler(i)                   
               xi = 'Re Installed'
            name = "modules.{}".format(cr)
            try:
              dr = importlib.util.spec_from_file_location(name, imodule)
              er = importlib.util.module_from_spec(dr)
              dr.loader.exec_module(er)
              await ss.edit(f"`{xi} module {os.path.basename(imodule)}`")        
            except:
              text = str(traceback.format_exc()) 
              if len(text) > 4096:               
                 with open("error.txt", "w+") as f:
                    f.write(text)
                 await event.reply(file="error.txt")
                 os.remove("error.txt")           
              else:
                 await ss.edit(text)  
            return os.remove(imodule)
    else:
     return await ss.edit("`[Error] reply to a plugin`")     
 
    

@handler(pattern="/install(?: |$)(.*)",admin=True,user=True)
async def install(event):
    ss = await event.reply("`Installing....`")
    xi = 'Installed'
    if event.reply_to_msg_id:
            imodule = await event.client.download_media(await event.get_reply_message())    
            cr = (os.path.splitext(os.path.basename(imodule))[0])
            if cr in cmd.keys(): 
               for i in cmd[cr]: 
                   event.client.remove_event_handler(i)                   
               xi = 'Re Installed'
            name = "modules.{}".format(cr)
            try:
              dr = importlib.util.spec_from_file_location(name, imodule)
              er = importlib.util.module_from_spec(dr)
              dr.loader.exec_module(er)
              await ss.edit(f"`{xi} module {os.path.basename(imodule)}`")        
            except:
              text = str(traceback.format_exc()) 
              if len(text) > 4096:               
                 with open("error.txt", "w+") as f:
                    f.write(text)
                 await event.reply(file="error.txt")
                 os.remove("error.txt")           
              else:
                 await ss.edit(text)  
            return os.remove(imodule)
    else:
     return await ss.edit("`[Error] reply to a plugin`")    

@handler(pattern="/ctask(?: |$)(.*)")
async def admin(event):
 try:
  ss = await event.reply("`processing...`") 
  cid = str((await event.get_sender()).id) 
  task = asyncio.current_task()
  tname = task.get_name()
  yc = 0
  id = str(event.pattern_match.group(1))
  if id:
   if cid in adm or cid in id:
     cid = id
  else:
   mid = await event.get_reply_message()
   mmid = None
   if mid:
     mid = (await mid.get_sender()).id
     if mid:
       mmid = mid
   if cid in adm and mmid:
     cid = str(mmid)
  xc = 0
  for task in asyncio.all_tasks():
      yc = yc + 1
      if cid in task.get_name() and not tname == task.get_name():
           task.cancel()
           xc = xc + 1
  await ss.edit(f"`Cleared {xc}/{yc} Task(s) ~ > {cid}`")    
 except asyncio.CancelledError:
    return
    




if tbot:
  tbot.start()

if pbot:
  pbot.start()  


dirc = "workdir"

if not os.path.exists(dirc):
    os.makedirs(dirc)
    
os.chdir(dirc)

from web import *


async def startup():
 await tbot.start()
 if user:
   await user.start()
   await user.send_message("@rekcah05","Started..")
 await tbot.send_message("@rekcah05","Started..")
 print("Started")
 config = uvicorn.Config("__main__:app", port=port,host="0.0.0.0", log_level="error")
 server = uvicorn.Server(config)
 print("all done")
 await server.serve()

async def startup2():
 await user.start()
 await user.send_message("@rekcah05","Started..")
 print("Started")
 config = uvicorn.Config("__main__:app", port=port,host="0.0.0.0", log_level="error")
 server = uvicorn.Server(config)
 print("all done")
 await server.serve()

if tbot:
  tbot.loop.run_until_complete(startup()) 
elif user:
  user.loop.run_until_complete(startup2())
else:
 raise ValueError("nothing")
  





