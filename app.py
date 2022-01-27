import os
from main import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from main.utils import weed_offers, db_backup


env = os.environ['ENV']
app = create_app(env)

app.app_context().push()

scheduler = BackgroundScheduler()
scheduler.add_job(weed_offers, 'interval', minutes=2, id='weed_transit')
scheduler.add_job(db_backup, 'interval',seconds = 5,id = 'backup_db')
scheduler.start()

if __name__ == '__main__':    
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port,use_reloader=False)