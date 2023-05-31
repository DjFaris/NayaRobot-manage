from pyrogram import filters

from pyrogram.types import Message
import os
import asyncio 
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from Naya.core.decorators.permissions import adminsOnly
from Naya.core.decorators.errors import capture_err
from pyrogram.errors import FloodWait
from Naya import *

chatQueue = []

stopProcess = False

@app.on_message(filters.command(["tagall","mentionall","all","mention"]))
@adminsOnly("can_change_info")
async def everyone(_, message):
  global stopProcess
  try: 
    try:
      sender = await app.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 500:
        await message.reply("-› Saya sudah mengerjakan jumlah maksimum 500 obrolan saat ini. Coba sebentar lagi.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("-› Sudah ada proses yang sedang berlangsung dalam obrolan ini. Silakan / stop untuk memulai yang baru.")
        else:  
          chatQueue.append(message.chat.id)
          if len(message.command) > 1:
            inputText = " ".join(message.command[1:])
          elif len(message.command) == 1:
            inputText = ""    
          membersList = []
          async for member in app.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"{inputText}\n\n"
            try:    
              while j < 10:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"{user.mention} "
                  j+=1
                else:
                  text1 += f"@{user.username} "
                  j+=1
              try:     
                await app.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(1) 
              i+=10
            except IndexError:
              try:
                await app.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"-› Berhasil menyebutkan **jumlah total {i} anggota**.\n-› Bot dan akun yang dihapus ditolak.") 
          else:
            await message.reply(f"-› Berhasil menyebutkan **{i} anggota.**\n-› Bot dan akun yang dihapus ditolak.")    
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("-› Maaf, **hanya admin** yang dapat menjalankan perintah ini.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                    
        
@app.on_message(filters.command(["stop","cancel"]))
@adminsOnly("can_change_info")
async def stop(_, message):
  global stopProcess
  try:
    try:
      sender = await app.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("-› Tidak ada proses yang berkelanjutan untuk dihentikan.")
      else:
        stopProcess = True
        await message.reply("-› Stopped.")
    else:
      await message.reply("-› Maaf, **hanya admin** yang dapat menjalankan perintah ini.")
  except FloodWait as e:
    await asyncio.sleep(e.value)
