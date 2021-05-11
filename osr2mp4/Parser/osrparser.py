from osr2mp4.osrparse import *
from osr2mp4.Parser import osuparser

# index for replay_event
from osr2mp4.CheckSystem.Judgement import DiffCalculator
# noinspection PyTypeChecker
from osr2mp4.EEnum.EReplay import Replays




def add_useless_shits(replay_data: list, beatmap: osuparser.Beatmap):
	for x in range(10):
		replay_data += [ReplayEvent(
			x = replay_data[-1].x,
			y = replay_data[-1].y,
			keys_pressed = 0,
			time = max(replay_data[-1].time, int(beatmap.end_time + 1000)) + 17*x
			)]


	diffcalculator = DiffCalculator(beatmap.diff)
	timepreempt = diffcalculator.ar()
	
	if replay_data[0].time > beatmap.hitobjects[0]["time"] - timepreempt - 2000:
		startdata = replay_data[0].copy()
		startdata.time = beatmap.hitobjects[0]["time"] - timepreempt - 2000
		replay_data.insert(0, startdata)

	replay_data.append(ReplayEvent(x=0, y=0, keys_pressed=0, time=replay_data[-1].time * 5))
	replay_data.append(ReplayEvent(x=0, y=0, keys_pressed=0, time=replay_data[-1].time * 5))

	beatmap.breakperiods.append(
		{
		"Start": int(beatmap.end_time + 200), 
		"End": replay_data[-1][Replays.TIMES] + 100, 
		"Arrow": False
		}
		)


def setup_replay(osrfile: str, beatmap: osuparser.Beatmap, reverse: bool = False):
	replay_info = parse_replay_file(osrfile)
	replay_data = replay_info.play_data

	start_time = beatmap.start_time

	start_osr = start_time - 3000

	replay_data = [r for r in replay_data if r.time > start_osr] # we dont need replay events before the
	replay_data = replay_data[:-1]								# map start_time
	replay_data.sort(key=lambda x: x.time) # prolly dont need this but just in case

	add_useless_shits(replay_data, beatmap)
	start_time = replay_data[0].time

	return replay_data, start_time
