import asyncio
import pandas as pd
# open the file in the write mode


# create the csv writer

from telethon import TelegramClient, connection
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (
    PeerChannel
)


# Setting configuration values
api_id = "Your API ID"                                                     
api_hash = "Your API hash"                            
api_hash = str(api_hash)
phone = "Your Phone number with Country code"
username="Your telegram username"

# Create the client and connect
client = TelegramClient(
    username,
    api_id,
    api_hash  )

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = "Your channel link"

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset = 0
    limit = 100
    all_participants = []

    while True:
        participants = await client(GetParticipantsRequest(
            my_channel, ChannelParticipantsSearch(''), offset, limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    all_user_details = []
    id=[]
    first_name=[]
    last_name= []
    usernames=[]
    numbers=[]
    access_hashes =[]
    for participant in all_participants:
        id.append(participant.id)
        first_name.append(participant.first_name)
        last_name.append(participant.last_name)
        usernames.append(participant.username)
        numbers.append(participant.phone)
        access_hashes.append(participant.access_hash)
        
        
        
    df= pd.DataFrame({"ID": id, "First Name": first_name, "Last Name": last_name, "Username": usernames, "Phone": numbers, "Access Hash": access_hashes})
    df.to_csv("participants.csv", index=True)
    #     all_user_details.append(
    #         {"id": participant.id, "first_name": participant.first_name, "last_name": participant.last_name,
    #          "user": participant.username, "phone": participant.phone, "access_hash": participant.access_hash})

    # with open('user_data.csv', 'w') as outfile:
    #     writer= csv.writer(outfile)
    #     writer.writerow()

        
        # json.dump(all_user_details, outfile)

with client:
    client.loop.run_until_complete(main(phone))