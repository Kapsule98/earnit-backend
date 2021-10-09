import os
from main.config import config_by_name
from main import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from main.utils import weed_offers

config = config_by_name['dev']

app = create_app('dev')

app.app_context().push()

scheduler = BackgroundScheduler()
scheduler.add_job(weed_offers, 'interval', minutes=2, id='weed_transit')
scheduler.start()

if __name__ == '__main__':    
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)