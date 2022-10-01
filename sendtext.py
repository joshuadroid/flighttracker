# Download the helper library from https://www.twilio.com/docs/python/install
import os
import pandas as pd
from twilio.rest import Client
from sqlalchemy import create_engine
from local_settings import account_sid, auth_token, messaging_service_sid, to_number, cronitor_api_key
import cronitor

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secu
client = Client(account_sid, auth_token)

cronitor.api_key = cronitor_api_key

#Or, you can embed telemetry events directly in your code
monitor = cronitor.Monitor('sendtext')
monitor.ping() # send a heartbeat event

engine = create_engine('sqlite:///freefolkposts.sqlite', echo=False)

new_df = pd.DataFrame(engine.execute('SELECT * FROM textlist ORDER BY Date DESC').fetchall())

for x in range(100):
    try:
        texted = new_df.loc[x, 'texted']
        print(texted)
        if texted == 'Y':
            continue
        else:
            preview_pic = new_df.loc[x, 'Preview Pic']
            title = new_df.loc[x, 'Title']
            post_date = new_df.loc[x, 'Date']
            print(f"Preview Pic is: {preview_pic} \
                    Title is: {title} \
                    Posted on: {post_date}")
            print(x)
            counter = x
        break
    except(KeyError):
        print('Made it to the end of the list!')
        break

#code to tick Y for texted items
print(counter)
new_df.loc[counter, 'texted'] = 'Y'
new_df = new_df.set_index("Link")
new_df.to_sql('textlist', con=engine, if_exists='replace')

message = client.messages \
            .create(
                body=f"{post_date}:{title} {preview_pic}",
                from_= messaging_service_sid,
                to=to_number
            )

m = message.sid

if not m:
    monitor.ping(state='fail')
else:
    print(message.sid)
    # the job has completed successfully
    monitor.ping(state='complete')