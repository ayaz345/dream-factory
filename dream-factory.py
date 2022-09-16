# Copyright 2021 - 2022, Bill Kennedy (https://github.com/rbbrdckybk/ai-art-generator)
# SPDX-License-Identifier: MIT

import threading
import time
import datetime
import shlex
import subprocess
import sys
import unicodedata
import re
import random
import os
import platform
import signal
import webbrowser
import argparse
import scripts.utils as utils
from os.path import exists
from datetime import datetime as dt
from datetime import date
from pathlib import Path
from collections import deque
from PIL.PngImagePlugin import PngImageFile, PngInfo
from torch.cuda import get_device_name, device_count
from scripts.server import ArtServer

# environment setup
cwd = os.getcwd()

if sys.platform == "win32" or os.name == 'nt':
    import keyboard
    os.environ['PYTHONPATH'] = os.pathsep + (cwd + "\latent-diffusion") + os.pathsep + (cwd + "\\taming-transformers") + os.pathsep + (cwd + "\CLIP")
else:
    os.environ['PYTHONPATH'] = os.pathsep + (cwd + "/latent-diffusion") + os.pathsep + (cwd + "/taming-transformers") + os.pathsep + (cwd + "/CLIP")

# Prevent threads from printing at same time.
print_lock = threading.Lock()


# worker thread executes specified shell command
class Worker(threading.Thread):
    def __init__(self, command, callback=lambda: None, *args):
        threading.Thread.__init__(self)
        self.command = command
        self.callback = callback

        # grab the worker info from the args
        self.worker = args[0]

        # grab the output buffer
        self.output_buffer = None
        if len(args) > 1:
            self.output_buffer = args[1]


    def run(self):
        if not self.command.get('seed') > 0:
            self.command['seed'] = random.randint(1, 2**32) - 1000

        # if this is a random prompt, settle on random values
        if self.command.get('mode') == 'random':
            self.command['scale'] = round(random.uniform(float(self.command.get('min_scale')), float(self.command.get('max_scale'))), 1)
            self.command['strength'] = round(random.uniform(float(self.command.get('min_strength')), float(self.command.get('max_strength'))), 2)
            if self.command.get('random_input_image_dir') != "":
                self.command['input_image'] = utils.InputManager(self.command.get('random_input_image_dir')).pick_random()

        command = utils.create_command(self.command, self.command.get('prompt_file'), self.worker['id'])
        self.print("starting job #" + str(self.worker['jobs_done']+1) + ": " + command)

        start_time = time.time()
        self.worker['job_start_time'] = start_time
        self.worker['job_prompt_info'] = self.command

        if control.config.get('debug_test_mode'):
            # simulate SD work
            work_time = round(random.uniform(5, 15), 2)
            time.sleep(work_time)
        else:
            # invoke SD
            if sys.platform == "win32" or os.name == 'nt':
                subprocess.call(shlex.split(command), cwd=(cwd + '\stable-diffusion'))
            else:
                subprocess.call(shlex.split(command), cwd=(cwd + '/stable-diffusion'))

        # TODO change /samples to /samples + gpu_id in forked SD repo
        output_dir = command.split(" --outdir ",1)[1].strip('\"')
        output_dir = output_dir.replace("../","")
        samples_dir = output_dir + "/samples"

        # upscale here if requested
        if self.command['use_upscale'] == 'yes':
            self.worker['work_state'] = 'upscaling'
            gpu_id = self.worker['id'].replace("cuda:", "")

            if control.config.get('debug_test_mode'):
                # simulate upscaling work
                work_time = round(random.uniform(3, 6), 2)
                time.sleep(work_time)

            else:
                new_files = os.listdir(samples_dir)
                if len(new_files) > 0:
                    if not control.config.get('debug_test_mode'):
                        # invoke ESRGAN on entire directory
                        utils.upscale(self.command['upscale_amount'], samples_dir, self.command['upscale_face_enh'], gpu_id)

                    # remove originals if upscaled version present
                    new_files = os.listdir(samples_dir)
                    for f in new_files:
                        if (".png" in f):
                            basef = f.replace(".png", "")
                            if basef[-2:] == "_u":
                                # this is an upscaled image, delete the original
                                # or save it in /original if desired
                                if exists(samples_dir + "/" + basef[:-2] + ".png"):
                                    if self.command['upscale_keep_org'] == 'yes':
                                        # move the original to /original
                                        orig_dir = output_dir + "/original"
                                        Path(orig_dir).mkdir(parents=True, exist_ok=True)
                                        os.replace(samples_dir + "/" + basef[:-2] + ".png", \
                                            orig_dir + "/" + basef[:-2] + ".png")
                                    else:
                                        os.remove(samples_dir + "/" + basef[:-2] + ".png")


        # find the new image(s) that SD created: re-name, process, and move them
        self.worker['work_state'] = "+exif data"
        if control.config.get('debug_test_mode'):
            # simulate metadata work
            work_time = round(random.uniform(1, 2), 2)
            time.sleep(work_time)
        else:
            new_files = os.listdir(samples_dir)
            nf_count = 0
            for f in new_files:
                if (".png" in f):
                    # save just the essential prompt params to metadata
                    meta_prompt = command.split(" --prompt ",1)[1]
                    meta_prompt = meta_prompt.split(" --outdir ",1)[0]

                    if 'seed_' in f:
                        # grab seed from filename
                        actual_seed = f.replace('seed_', '')
                        actual_seed = actual_seed.split('_',1)[0]

                        # replace the seed in the command with the actual seed used
                        pleft = meta_prompt.split(" --seed ",1)[0]
                        pright = meta_prompt.split(" --seed ",1)[1].strip()
                        meta_prompt = pleft + " --seed " + actual_seed

                    upscale_text = ""
                    if self.command['use_upscale'] == 'yes':
                        upscale_text = " (upscaled "
                        upscale_text += str(self.command['upscale_amount']) + "x via "
                        if self.command['upscale_face_enh'] == 'yes':
                            upscale_text += "ESRGAN/GFPGAN)"
                        else:
                            upscale_text += "ESRGAN)"

                    pngImage = PngImageFile(samples_dir + "/" + f)
                    im = pngImage.convert('RGB')
                    exif = im.getexif()
                    exif[0x9286] = meta_prompt
                    exif[0x9c9c] = meta_prompt.encode('utf16')
                    exif[0x9c9d] = ('AI art' + upscale_text).encode('utf16')
                    exif[0x0131] = "https://github.com/rbbrdckybk/dream-factory"
                    newfilename = dt.now().strftime('%Y%m-%d%H-%M%S-') + str(nf_count)
                    nf_count += 1
                    im.save(output_dir + "/" + newfilename + ".jpg", exif=exif, quality=88)
                    if exists(samples_dir + "/" + f):
                        os.remove(samples_dir + "/" + f)


        self.worker['work_state'] = ""
        # remove the /samples dir if empty
        try:
            os.rmdir(samples_dir)
        except OSError as e:
            pass


        exec_time = time.time() - start_time
        self.print("finished job #" + str(self.worker['jobs_done']+1) + " in " + str(round(exec_time, 2)) + " seconds.")
        self.callback(self.worker)


    def print(self, text):
        out_txt = "[" + self.worker['id'] + "] >>> " + text
        with print_lock:
            print(out_txt)

        # also write to buffer for webserver use
        if self.output_buffer != None:
            self.output_buffer.append(out_txt + '\n')


# controller manages worker thread(s) and user input
# TODO change worker_idle to array of bools to manage multiple threads/gpus
class Controller:
    def __init__(self, config_file):

        self.config_file = config_file
        self.config = {}
        self.prompt_file = ""

        self.prompt_manager = None
        self.input_manager = None

        self.output_buffer = deque([], maxlen=300)
        self.work_queue = deque()
        self.workers = []
        self.work_done = False
        self.is_paused = False
        self.loops = 0
        self.orig_work_queue_size = 0
        self.jobs_done = 0
        self.total_jobs_done = 0
        self.repeat_jobs = False
        self.server = None
        self.server_startup_time = time.time()

        signal.signal(signal.SIGINT, self.sigterm_handler)
        signal.signal(signal.SIGBREAK, self.sigterm_handler)
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        # read config options
        self.init_config()

        # start the webserver if enabled
        if self.config.get('webserver_use'):
            x = threading.Thread(target=self.start_server, args=(), daemon=True)
            x.start()

        if not self.config.get('debug_test_mode'):
            # initialize GPU(s)
            self.init_gpu_workers()
        else:
            # create some dummy devices for testing
            self.init_dummy_workers()


    # returns the current operation mode (combination or random)
    def get_mode(self):
        if self.prompt_manager != None:
            return self.prompt_manager.config.get('mode')
        else:
            return None

    # reads the config file
    def init_config(self):
        # set defaults
        self.config = {
            'prompts_location' : 'prompts',
            'output_location' : 'output',
            'use_gpu_sevices' : 'auto',
            'webserver_use' : True,
            'webserver_port' : 8080,
            'webserver_open_browser' : True,
            'webserver_console_log' : False,
            'debug_test_mode' : False
        }

        file = utils.TextFile(self.config_file)
        if file.lines_remaining() > 0:
            self.print("reading configuration from " + self.config_file + "...")
            while file.lines_remaining() > 0:
                line = file.next_line()

                # update config values for found directives
                if '=' in line:
                    line = line.split('=', 1)
                    command = line[0].lower().strip()
                    value = line[1].strip()

                    if command == 'prompts_location':
                        if value != '':
                            self.config.update({'prompts_location' : value})

                    elif command == 'output_location':
                        if value != '':
                            self.config.update({'output_location' : value})

                    elif command == 'use_gpu_devices':
                        if value != '':
                            self.config.update({'use_gpu_devices' : value})

                    elif command == 'webserver_use':
                        if value == 'yes' or value == 'no':
                            if value == 'yes':
                                self.config.update({'webserver_use' : True})
                            else:
                                self.config.update({'webserver_use' : False})

                    elif command == 'webserver_port':
                        try:
                            int(value)
                        except:
                            print("*** WARNING: specified 'WEBSERVER_PORT' is not a valid number; it will be ignored!")
                        else:
                            self.config.update({'webserver_port' : int(value)})

                    elif command == 'webserver_open_browser':
                        if value == 'yes' or value == 'no':
                            if value == 'yes':
                                self.config.update({'webserver_open_browser' : True})
                            else:
                                self.config.update({'webserver_open_browser' : False})

                    elif command == 'webserver_console_log':
                        if value == 'yes' or value == 'no':
                            if value == 'yes':
                                self.config.update({'webserver_console_log' : True})
                            else:
                                self.config.update({'webserver_console_log' : False})

                    elif command == 'debug_test_mode':
                        if value == 'yes' or value == 'no':
                            if value == 'yes':
                                self.config.update({'debug_test_mode' : True})
                            else:
                                self.config.update({'debug_test_mode' : False})

                    else:
                        self.print("warning: config file command not recognized: " + command.upper() + " (it will be ignored)!")


        else:
            self.print("configuration file '" + self.config_file + "' doesn't exist; using defaults...")


    # starts the webserver
    def start_server(self):
        addr = "http://localhost"
        if self.config['webserver_port'] != 80:
            addr += ':' + str(self.config['webserver_port']) + '/'
        self.print("starting webserver (" + addr + ") as a background process...")
        if self.config.get('webserver_open_browser'):
            webbrowser.open(addr)
        self.server = ArtServer()
        self.server.start(self)


    # handle graceful cleanup here
    def sigterm_handler(self, signal, frame):
        # save the state here or do whatever you want
        self.print('********** Exiting; handling clean up ***************')
        self.shutdown()
        sys.exit(0)


    # resizes the output_buffer
    def resize_buffer(self, new_length):
        self.output_buffer = deque([], maxlen=new_length)


    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.print("Pause requested; workers will finish current work and then wait...")


    def unpause(self):
        if self.is_paused:
            self.is_paused = False
            self.print("Un-pausing; workers will resume working...")


    def shutdown(self):
        self.print("Server shutdown requested; cleaning up and shutting down...")
        if self.server != None:
            # stop the webserver if it's running
            self.server.stop()
        self.is_paused = True
        self.work_done = True


    # adds a GPU to the list of workers
    def add_gpu_worker(self, id, name):
        self.workers.append({'id': id, \
            'name': name, \
            'work_state': "", \
            'jobs_done': 0, \
            'job_prompt_info': '', \
            'job_start_time': float(0), \
            'idle': True})
        self.print("initialized worker '" + id + "': " + name)


    # build a list of gpu workers
    def init_gpu_workers(self):
        if self.config['use_gpu_devices'] == "auto":
            # attempt to auto-detect GPUs
            self.print("detected " + str(device_count()) + " total GPU device(s)...")
            for i in range(device_count()):
                name = ""
                worker = "cuda:" + str(i)
                try:
                    name = get_device_name(worker)
                except AssertionError:
                    self.print("unable to initialize device '" + worker + "'; removing it as a GPU candidate...")

                # if we can see the gpu name, add it to the list of workers
                if name != '':
                    self.add_gpu_worker(worker, name)

        elif ',' in self.config['use_gpu_devices']:
            # we're specifying individual GPUs
            gpus = self.config['use_gpu_devices'].split(',')
            for gpu in gpus:
                name = ""
                worker = "cuda:" + gpu.strip()
                try:
                    name = get_device_name(worker)
                except AssertionError:
                    self.print("unable to initialize device '" + worker + "'; removing it as a GPU candidate...")

                # if we can see the gpu name, add it to the list of workers
                if name != '':
                    self.add_gpu_worker(worker, name)

        else :
            self.print("ERROR: can't understand USE_GPU_DEVICES configuration: " + self.config['use_gpu_devices'])


    # build a list of dummy workers for debugging/testing
    def init_dummy_workers(self):
        worker_list = []
        worker_list.append("cuda:0")
        worker_list.append("cuda:1")
        worker_list.append("cuda:2")
        worker_list.append("cuda:3")
        #worker_list.append("cpu")

        for worker in worker_list:
            worker = worker.lower().strip()
            name = ''
            if ':' in worker:
                if worker.split(':' ,1)[0] == 'cuda':
                    try:
                        name = get_device_name(worker)
                    except AssertionError:
                        name = "Dummy GPU Device"

            elif worker == 'cpu':
                name = platform.processor()

            # if we're able to see the device, add it to the worker queue
            if name != '':
                self.add_gpu_worker(worker, name)


    # returns the first idle gpu worker if there is one, otherwise returns None
    def get_idle_gpu_worker(self):
        for worker in self.workers:
            if ':' in worker["id"]:
                if worker["id"].split(':' ,1)[0] == 'cuda':
                    # this is a gpu worker
                    if worker["idle"]:
                        # worker is idle, return it
                        return worker

        # none of the gpu workers are idle
        return None


    # returns the current number of working workers
    def num_workers_working(self):
        working = 0
        for worker in self.workers:
            if not worker["idle"]:
                working += 1
        return working


    # start a new worker thread
    def do_work(self, worker, command):
        worker['idle'] = False
        thread = Worker(command, self.work_done_callback, worker, self.output_buffer)
        thread.start()


    # callback for worker threads when finished
    def work_done_callback(self, *args):
        self.jobs_done += 1
        self.total_jobs_done += 1
        # args[0] contains worker data; set this worker back to idle
        args[0]['idle'] = True
        args[0]['work_state'] = ""
        args[0]['jobs_done'] += 1
        args[0]['job_start_time'] = 0
        args[0]['job_prompt_info'] = ''



    def clear_work_queue(self):
        self.print("clearing work queue...")
        self.work_queue.clear()
        self.loops = 0
        self.jobs_done = 0
        self.orig_work_queue_size = 0


    # build a work queue with the specified prompt and style files
    def init_work_queue(self):
        # random mode; queue up a few random prompts
        if self.prompt_manager.config.get('mode') == 'random':
            for i in range(50):
                #work = "Test work item #" + str(i+1)
                work = self.prompt_manager.config.copy()
                work['prompt'] = self.prompt_manager.pick_random()
                work['prompt_file'] = self.prompt_file
                self.work_queue.append(work)

        # combination mode, grab all possible combos
        else:
            self.work_queue = self.prompt_manager.build_combinations()
            self.orig_work_queue_size = len(self.work_queue)


        self.print("queued " + str(len(self.work_queue)) + " work items.")



    # loads a new prompt file
    # note that new_file is an absolute path reference
    def new_prompt_file(self, new_file):
        # TODO validate everything is ok before making the switch
        self.prompt_file = new_file
        self.prompt_manager = utils.PromptManager(self)

        self.prompt_manager.handle_config()
        self.input_manager = utils.InputManager(self.prompt_manager.config.get('random_input_image_dir'))

        self.clear_work_queue()
        self.init_work_queue()








    # for debugging; prints a report of current worker status
    def print_worker_report(self):
        i = 0
        self.print("*** Worker Report ***")
        for worker in self.workers:
            i += 1
            self.print("Worker #" + str(i) + ":")
            for k, v in worker.items():
                if isinstance(v, str):
                    self.print("   " + k + ": '" + str(v) + "'")
                else:
                    self.print("   " + k + ": " + str(v))

    def print(self, text):
        out_txt = "[controller] >>> " + text
        with print_lock:
            print(out_txt)
        # also write to buffer for webserver use
        self.output_buffer.append(out_txt + '\n')


# entry point
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        type=str,
        nargs="?",
        default="config.txt",
        help="the server configuration file"
    )

    parser.add_argument(
        "--prompt_file",
        type=str,
        nargs="?",
        default="",
        help="initial prompt file to load"
    )

    opt = parser.parse_args()
    control = Controller(opt.config)
    if len(control.workers) == 0:
        control.print("ERROR: unable to initialize any GPUs for work; exiting!")
        exit()

    # load initial prompt file if specified
    if (opt.prompt_file) != "":
        if exists(opt.prompt_file):
            control.new_prompt_file(opt.prompt_file)
        else:
            control.print("ERROR: specified prompt file '" + opt.prompt_file + "' does not exist - load one from the control panel instead!")

    # main work loop
    while not control.work_done:
        # check for idle workers
        worker = control.get_idle_gpu_worker()
        if worker != None:
            # worker is idle, start some work
            if not control.is_paused:
                if len(control.work_queue) > 0:
                    # get a new prompt or setting directive from the queue
                    new_work = control.work_queue.popleft()
                    control.do_work(worker, new_work)
                else:
                    # if we're in random prompts mode, re-fill the queue
                    if control.prompt_manager != None and control.prompt_manager.config.get('mode') == 'random':
                        control.print('adding more random prompts to the work queue...')
                        control.init_work_queue()
                    else:
                        if not control.repeat_jobs:
                            control.is_paused = True
                            # no more jobs, wait for all workers to finish
                            control.print('No more work in queue; waiting for all workers to finish...')
                            while control.num_workers_working() > 0:
                                time.sleep(.01)
                            control.print('All work done; pausing server - add some more work via the control panel!')
                        else:
                            # flag to repeat work enabled, re-load work queue
                            control.loops += 1
                            control.jobs_done = 0
                            control.init_work_queue()

        else:
            time.sleep(.01)

    print('\nShutting down...')
    if control and control.total_jobs_done > 0:
        print("\nTotal jobs done: " + str(control.total_jobs_done))
        #control.print_worker_report()

    exit()
