from apscheduler.schedulers.blocking import BlockingScheduler

def classify_and_model():
	#preprocess
	

sched = BlockingScheduler()
sched.add_job(classify_and_model, 'interval', minutes = 15)
sched.start()