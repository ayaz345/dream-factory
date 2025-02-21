# Dream Factory



Multi-threaded GUI manager for mass creation of AI-generated art with support for multiple GPUs.

This is aimed at the user that wants to create a **lot** of AI artwork with minimal hands-on time. If you're looking for a repo that will allow you to spend hours tweaking a single image until it's perfect, [there are better options](https://github.com/AUTOMATIC1111/stable-diffusion-webui) (update 2022-12-06: Dream Factory now uses Automatic1111's repo on the backend so you'll get the best of both worlds!). If you have hundreds of prompt ideas and want to easily and quickly (well, as quickly as your GPUs can manage!) see them rendered in hundreds of different variations and/or styles, then this is for you.

To illustrate, I've had three GPUs running Dream Factory unattended virtually 24/7 for a few months — they churn out thousands of images every day! I can check on my images and make modifications to my running jobs remotely, at my convenience, via the Dream Factory web UI. Some samples (all straight out of Dream Factory other than reducing resolution to 1024x1024):  
<table>
 <tr>
  <td><img src="/images/01.jpg" width="152" height="152" alt="sample image 1" title="sample image 1"></td>
  <td><img src="/images/02.jpg" width="152" height="152" alt="sample image 2" title="sample image 2"></td>
  <td><img src="/images/03.jpg" width="152" height="152" alt="sample image 3" title="sample image 3"></td>
  <td><img src="/images/04.jpg" width="152" height="152" alt="sample image 4" title="sample image 4"></td>
 </tr>
 <tr>
  <td><img src="/images/05.jpg" width="152" height="152" alt="sample image 5" title="sample image 5"></td>
  <td><img src="/images/06.jpg" width="152" height="152" alt="sample image 6" title="sample image 6"></td>
  <td><img src="/images/07.jpg" width="152" height="152" alt="sample image 7" title="sample image 7"></td>
  <td><img src="/images/08.jpg" width="152" height="152" alt="sample image 8" title="sample image 8"></td>
 </tr>
 <tr>
  <td><img src="/images/09.jpg" width="152" height="152" alt="sample image 9" title="sample image 9"></td>
  <td><img src="/images/10.jpg" width="152" height="152" alt="sample image 10" title="sample image 10"></td>
  <td><img src="/images/11.jpg" width="152" height="152" alt="sample image 11" title="sample image 11"></td>
  <td><img src="/images/12.jpg" width="152" height="152" alt="sample image 12" title="sample image 12"></td>
 </tr>
</table>

Some UI screenshots:
<table>
 <tr>
  <td><img src="/images/screen_monitor.png" width="152" height="152" alt="UI: status monitor" title="UI: status monitor"></td>
  <td><img src="/images/screen_editor.png" width="152" height="152" alt="UI: prompt editor" title="UI: prompt editor"></td>
  <td><img src="/images/screen_gallery.png" width="152" height="152" alt="UI: gallery" title="UI: gallery"></td>
  <td><img src="/images/screen_gallery_image.png" width="152" height="152" alt="UI: image viewer" title="UI: image viewer"></td>
 </tr>
</table>

# Features

 * Based on [Stable Diffusion](https://stability.ai/blog/stable-diffusion-public-release).
 * Dream Factory acts as a powerful automation and management tool for the popular [Automatic1111 SD repo](https://github.com/AUTOMATIC1111/stable-diffusion-webui#features). Integration with Automatic1111's repo means Dream Factory has access to one of the most full-featured Stable Diffusion packages available.
 * Multi-threaded engine capable of simultaneous, fast management of multiple GPUs. As far as I'm aware, Dream Factory is currently one of the only Stable Diffusion options for true multi-GPU support.
 * Powerful custom prompt file format that allows you to easily define compound prompt templates. Want to quickly create thousands of prompts from a template like "_photo of a **[adjective(s)] [animal]** as a **[profession]**, art by **[artist(s)]**, **[keyword(s)]**_" where each bracketed section needs to be filled in with dozens (or hundreds) of different items? No problem. Maybe you want your GPUs to create every possible combination, or maybe you want combinations to be picked randomly? Your choice. Maybe you want some items to be handled with different settings? Totally doable. Prompt files can be as complex or simple as you want — you can simply paste in a list of stand-alone prompts and go, too!
 * Dream Factory can automatically add custom model trigger word(s) to your prompts. For example, if you're using [this Modern Disney Style model](https://huggingface.co/nitrosocke/mo-di-diffusion), you need to add 'modern disney style' to each of your prompts. If you use a lot of custom models, it can be difficult to always remember to do this. Let Dream Factory handle it for you!
 * All prompt and creation settings are automatically embedded into output images as EXIF metadata (including the random seed used). Never wonder how you created an image again!
 * Easy web interface. Includes a built-in prompt file editor with context-sensitive highlighting, a gallery that displays your prompts and creation settings alongside your images, and at-a-glance information about the status of completed/ongoing work. Hate web interfaces? Turn it off via a configuration file — Dream Factory can be run completely via the command line if that's your thing!
 * Remote management. Access and fully manage your Dream Factory installation from anywhere (and easily download your created images in bulk as .zip files!). Can be configured to be accessible via LAN, WAN (internet), or just locally on the computer that Dream Factory is running on. Includes very basic HTTP-based authentication for WAN access.
 * Integration with [civitai.com](https://civitai.com/) within Dream Factory's prompt editor. All of your downloaded models, LoRAs, embeddings, hypernets will display relevant information (SD version compatibility, trigger words, etc) when available from Civitai. Can be disabled via Dream Factory's config file if you're running offline.
 * Integrated optional [ESRGAN upscaling](https://github.com/xinntao/ESRGAN) with [GFPGAN face correction](https://xinntao.github.io/projects/gfpgan). 
 * A special prompt file type for batch processing of existing images: automated upscaling, IPTC metadata tagging, image renaming, etc!
 * Easy setup. If you can download a file and copy & paste a few lines ([see below](https://github.com/rbbrdckybk/dream-factory/tree/main/README.md#setup)), you can get this working. Uses Anaconda so Dream Factory will happily run alongside other Stable Diffusion repos without disturbing them.

# Requirements

You'll need at least one Nvidia GPU, preferably with a decent amount of VRAM. 3GB of VRAM should be enough to produce 512x512 images, but more GPU memory will allow you to create larger images (and/or create them faster).

You'll also need a working [Automatic1111 Stable Diffusion webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui#installation-and-running).

# Setup

These instructions were tested on several Windows 10 desktops with a variety of modern Nvidia GPUs ranging from 8-12GB VRAM, and also on an Ubuntu Server 20.04.3 system with an old Nvidia Tesla M40 GPU (24GB VRAM).

**[1]** Install [Anaconda](https://www.anaconda.com/products/individual), open the root terminal, and create a new environment (and activate it):
```
conda create --name dream-factory python=3.9
conda activate dream-factory
```

**[2]** Install a couple required Python packages:
```
conda install -c anaconda git urllib3
```

**[3]** Clone this repository and switch to its directory:
```
git clone https://github.com/rbbrdckybk/dream-factory
cd dream-factory
```

**[4]** Run the included setup script to finish the rest of your installation automatically:
```
python setup.py
```

**[5]** Edit your config.txt file to specify the full path to your Automatic1111 SD installation:
 * Look for the **SD_LOCATION =** entry near the top of the file.
 * On Windows, it should look something like **SD_LOCATION = C:\Applications\stable-diffusion-webui** when finished, depending on where you placed Automatic1111's webui.
 * On Linux, you'll want something like **SD_LOCATION = /home/[username]/stable-diffusion-webui**, where [username] is the linux user it was installed under, assuming you kept the default install location.

You're done! Ensure that your [Automatic1111 installation works properly](https://github.com/AUTOMATIC1111/stable-diffusion-webui#installation-and-running) before attempting to test Dream Factory. Additionally, ensure that everything in the "settings" tab of Auto1111 is configured to your liking, as Dream Factory will automatically inherit any options you set there.

Once you've verified that you can generate individual images with your Auto1111 installation, you can perform a test to make sure Dream Factory is working by running this (again, from the main **dream-factory** folder):
```
python dream-factory.py --prompt_file prompts/example-standard.prompts
```
This should start up the web interface with a simple example prompt file pre-loaded that your GPU(s) should start working on automatically. On the first run, several large files (~2GB total) will be downloaded automatically so it may take a few minutes before things start happening.

Eventually you should see images appearing in your **\output** folder (or you can click on the "Gallery" link within the web UI and watch for them there). If you're getting images, everything is working properly and you can move on to the next section.

# Usage

Instructions assume that you've completed [setup](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#setup) and verified that your installation works properly.

## Startup and Basic Usage

Start Dream Factory with:
```
python dream-factory.py
```
The web UI should open automatically, if not go to http://localhost:8080 (assuming you didn't change the port in config.txt) via your browser. Your GPU(s) will automatically start initializing (each GPU will take about as long as it takes to launch auto1111 in standalone mode).

Browse to 'Control Panel' in the top nav and select one of the two example prompt files via the dropdown. Your GPU(s) should start working on whichever one you choose as soon as they're finished initializing. You can browse back to 'Status Monitor' and should see that your GPU(s) are being assigned work from the selected prompt file. If you browse to 'Gallery' in the top nav you'll see images appearing as they're completed.

## Creating and Editing Prompt Files

Prompt files are the heart of Dream Factory and define the work that you want your GPU(s) to do. They can be as simple or as complex as you want.

### Example Prompt Files

Before we get into creating new prompt files, let's take a look at the two example prompt files that are included with Dream Factory. Start by clicking 'Prompt Editor' in the top nav, then choose 'example-standard' in the 'Choose a prompt file:' dropdown.

You should see the prompt file load into the editor. Prompt files have an optional [config] section at the top with directives that define your Stable Diffusion settings, and at least one [prompts] section that contains prompts (or sections of prompts to be combined with other [prompts] sections).

The example files contain comments that should make it fairly clear what each [config] directive does, and how the [prompts] sections will combine. See the [Command Reference](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#prompt-file-command-reference) below for help on any directives that aren't clear.

### Creating a New Prompt File

You can create prompt files by using the integrated editor (click 'Prompt Editor' in the top nav, then click 'New Standard' or 'New Random' to start a new file). Prompt files will automatically be created with a skeleton containing common directives and the default settings contained in your config.txt.

After creation, prompt files can be renamed by simply clicking on the name at the top of the editor, entering a new name, and then clicking 'Rename'.

If you'd prefer, you can also create prompt files externally using a text editor of your choice (name them with a .prompt extension and place them in your prompts folder). If you happen to use [Notepad++](https://notepad-plus-plus.org/), there is a plugin in the **dream-factory/prompts/notepad_plugin** folder that will add context-sensitive highlighting to .prompt files.

### Prompt File Command Reference

These directives are valid only in the [config] section of both standard and random prompt files:

 * [!MODE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#mode)
 * [!DELIM](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#delim)

These directives are valid in both the [config] section of both standard and random prompt files **and** also in any [prompts] section of **standard** prompt files (!MODE = standard):

 * [!WIDTH](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#width)
 * [!HEIGHT](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#height)
 * [!HIGHRES_FIX](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#highres_fix)
 * [!STEPS](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#steps)
 * [!SAMPLER](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#sampler)
 * [!SCALE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#scale)
 * [!SAMPLES](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#samples)
 * [!BATCH_SIZE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#batch_size)
 * [!INPUT_IMAGE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#input_image)
 * [!STRENGTH](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#strength)
 * [!CKPT_FILE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#ckpt_file)
 * [!NEG_PROMPT](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#neg_prompt)
 * [!AUTO_INSERT_MODEL_TRIGGER](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#auto_insert_model_trigger)
 * [!SEED](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#seed)
 * [!USE_UPSCALE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#use_upscale)
 * [!UPSCALE_MODEL](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#upscale_model)
 * [!UPSCALE_AMOUNT](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#upscale_amount)
 * [!UPSCALE_CODEFORMER_AMOUNT](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#upscale_codeformer_amount)
 * [!UPSCALE_GFPGAN_AMOUNT](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#upscale_gfpgan_amount)
 * [!UPSCALE_KEEP_ORG](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#upscale_keep_org)
 * [!FILENAME](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#filename)
 * [!CONTROLNET_INPUT_IMAGE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#controlnet_input_image)
 * [!CONTROLNET_MODEL](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#controlnet_model)
 * [!CONTROLNET_PRE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#controlnet_pre)
 * [!CONTROLNET_GUESSMODE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#controlnet_guessmode)
 * [!CONTROLNET_CONTROLMODE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#controlnet_controlmode)
 * [!CONTROLNET_PIXELPERFECT](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#controlnet_pixelperfect)
 * [!CONTROLNET_LOWVRAM](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#controlnet_lowvram)
 * [!AUTO_SIZE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#auto_size)
 * [!CLIP_SKIP](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#clip_skip)
 * [!SEAMLESS_TILING](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#seamless_tiling)
 * [!IPTC_TITLE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#iptc_title)
 * [!IPTC_DESCRIPTION](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#iptc_description)
 * [!IPTC_KEYWORDS](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#iptc_keywords)
 * [!IPTC_COPYRIGHT](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#iptc_copyright)
 
These directives are valid only in the [config] section of **standard** prompt files (!MODE = standard):

 * [!REPEAT](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#repeat)
 * [!NEXT_PROMPT_FILE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#next_prompt_file)

Finally, these directives are valid only in the [config] section of **random** prompt files (!MODE = random):

 * [!MIN_SCALE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#min_scale)
 * [!MAX_SCALE](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#max_scale)
 * [!MIN_STRENGTH](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#min_strength)
 * [!MAX_STRENGTH](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#max_strength)
 * [!RANDOM_INPUT_IMAGE_DIR](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#random_input_image_dir)

Command Help and Usage Examples:

#### !MODE
Sets the prompt file mode to either **standard** (default) or **random**. Standard prompt files work by iterating through all possible [prompts] sections combinations, and random prompt files simply pick prompts at random from [prompts] sections. See [prompts/example-standard.prompts](https://github.com/rbbrdckybk/dream-factory/blob/main/prompts/example-standard.prompts) and [prompts/example-random.prompts](https://github.com/rbbrdckybk/dream-factory/blob/main/prompts/example-random.prompts) for a detailed walkthrough of how each mode works.
```
!MODE = standard
```
Note that a third option for !MODE exists (**!MODE = process**) that enables advanced users to set up batch processing tasks on existing images (e.g.: batch upscaling, metadata tagging, renaming, etc) using Dream Factory. You can see an [example process .prompts file here](https://github.com/rbbrdckybk/dream-factory/blob/main/prompts/example-process.prompts).
#### !DELIM
Sets the delimiter that will be used when joining [prompts] sections (default is a space). For example, if you have two [prompts] sections, and the top entry in the first is "a portrait of" and the top entry in the second is "a cat", then when the two sections are combined, you'd end up with "a portrait of a cat" if !DELIM = " ". 
```
!DELIM = " "
```
#### !WIDTH
Sets the output image width, in pixels (default is 512). Note that this must be a multiple of 64!
```
!WIDTH = 512
```
#### !HEIGHT
Sets the output image height, in pixels (default is 512). Note that this must be a multiple of 64!
```
!HEIGHT = 512
```
#### !HIGHRES_FIX
Enables or disables the Auto1111 [highres fix](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#highres-fix). Valid options are **yes** or **no** (default). This should be enabled when generating images at resolutions signficantly higher than 512x512.
```
!HIGHRES_FIX = no
```
#### !STEPS
The number of denoising steps (default = 20). More steps will generally improve image quality to a point, at the cost of processing time.
```
!STEPS = 20
```
You may also specify a range (e.g. !STEPS = 30-55) and a random value within your range will be chosen when the prompt is executed.
#### !SAMPLER
The sampler to use (default is DPM++ 2M Karras). This must match an available option in your Auto1111 SD webui exactly. You can press ctrl+h or click the help icon at the top right corner of the editor to see a reference list of available samplers (click on a sampler to copy it to the clipboard so that you can easily paste it into the editor).
```
!SAMPLER = DPM++ 2M Karras
```
#### !SCALE
The guidance scale, or how closely you want Stable Diffusion to follow your text prompt. The default is 7.5, and generally speaking useful values are between 5 - 30.
```
!SCALE = 7.5
```
You may also specify a range (e.g. !SCALE = 5.5 - 9) and a random value within your range will be chosen when the prompt is executed.
#### !SAMPLES
How many images to produce of each prompt before moving on to the next one (default = 1). Unlike the below BATCH_SIZE option, there is no additional cost in terms of GPU memory when increasing this. There will be a liner increase in processing time when increasing this (e.g.: !SAMPLES = 10 will take ten times as long as !SAMPLES = 1).
```
!SAMPLES = 1
```
#### !BATCH_SIZE
How many images you want each GPU to produce in parallel (default = 1). Each increase of BATCH_SIZE will require more GPU VRAM, and setting this value too high will cause GPUs to run out of memory and crash. However, as long as you know you have enough VRAM, you can achieve moderate speed gains by increasing this beyond 1. This is an advanced setting and isn't included in new prompt file templates, however you may manually add it to your prompt files.
```
!BATCH_SIZE = 1
```
#### !INPUT_IMAGE
Sets an image to use as a starting point for the denoising process, rather than the default random noise. This can be a relative (to the Dream Factory base directory) or absolute path, and setting this to nothing will clear any previously-set input image.
```
!INPUT_IMAGE = C:\images\dog.png                         # specifies the full path to an input image
!INPUT_IMAGE = cat.jpg                                   # specifies an input image 'cat.jpg' in the DF home directory
!INPUT_IMAGE =                                           # specifies no input image should be used
```
Note that you may also pass a directory of images to this directive:
```
!INPUT_IMAGE = C:\images
```
If a directory is passed, every image in the folder will be applied to the prompt(s) that follow.
#### !STRENGTH
Sets the strength of the input image influence. Valid values are 0-1 (default = 0.75). Values close to 0 will result in an output image very similar to the input image, and values close to 1 will result in images with less resemblence. Generally, values between 0.2 - 0.8 are most useful. Note that this is also used when !HIGHRES_FIX = yes to indicate how closely the final image should mirror the low-res initialization image.
```
!STRENGTH = 0.75
```
You may also specify a range (e.g. !STRENGTH = 0.55 - 0.75) and a random value within your range will be chosen when the prompt is executed.
#### !CKPT_FILE
Sets the model to use. Any custom models should be installed to the appropriate models directory of your auto1111 installation. You can press ctrl+h or click the help icon at the top right corner of the editor to see a reference list of available models (click on a model to copy it to the clipboard so that you can easily paste it into the editor). Setting this to nothing will default back to whatever model you have set in your config.txt file (if you haven't set a default, setting this to nothing won't do anything!).

You many also set a list of comma-separated models here. In standard mode, Dream Factory will render all prompts with the first model, then the second, and so on. In random mode, Dream Factory will switch models every 50 prompts (this interval can be changed in your config.txt file).

You may also use the reserved word "all" here, and Dream Factory will rotate through all of your available models automatically.

**Note that you may only specify more than one model in the [config] section; model rotation is not supported anywhere else!**
```
!CKPT_FILE = analog-style.ckpt                           # sets a new model to use
!CKPT_FILE = sd-v1-5-vae.ckpt, analog-style.ckpt         # sets 2 models to rotate between
!CKPT_FILE = all                                         # will rotate between all of your models
!CKPT_FILE =                                             # sets the default model specified in your config.txt
```
Note: this uses a substring match on the valid server values available via the integrated reference, so for example if 'SD_1.5\dreamshaper_4BakedVae.safetensors [7f16bbcd80]' is what the reference reports, then setting **!CKPT_FILE = dreamshaper_4BakedVae.safetensors** will find it.
#### !NEG_PROMPT
Specifies a negative prompt to be used for all of the prompts that follow it (remember you can place most directives directly into [prompts] sections of standard prompt files!). If you have a 'catch-all' negative prompt that you tend to use, you can specify it in your config.txt file and it'll be populated as the default on new prompt files you create. Setting this to nothing will clear the negative prompt.
```
!NEG_PROMPT = watermark, blurry, out of focus
```
#### !AUTO_INSERT_MODEL_TRIGGER
For use with custom models that require a 'trigger word' that has been set up in your model-triggers.txt file (see [Custom Models](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#custom-models) below). This allows you to control the placement of the automatically-inserted trigger word. Valid options are **start** (default), **end**, **first_comma**, **keyword:[keyword to replace]** and **off**: 'start' will put the trigger word at the front of the prompt, 'end' will place it at the end, 'first_comma' will place it after the first comma (or at the end if there is no comma in the prompt), 'keyword:' will replace the specified keyword/phrase in the prompt with the model trigger word, and 'off' will disable auto-insertion entirely.
```
!AUTO_INSERT_MODEL_TRIGGER = start
```
#### !SEED
Specifies the seed value to be used in image creation. This value is normally chosen at random - using the same settings with the same seed value should produce exactly the same output image. Setting this to nothing will indicate that random seed values should be used (the default). This is an advanced setting and isn't included in new prompt file templates, however you may manually add it to your prompt files.
```
!SEED = 42
```
#### !USE_UPSCALE
Whether or not every output image should automatically be upscaled. Upscaling can take a significant amount of time, so generally you'd only want to do this on a subset of selected images. Valid options are **yes** or **no** (default).
```
!USE_UPSCALE = no
```
#### !UPSCALE_MODEL
Sets the upscaling model to use.
```
!UPSCALE_MODEL = esrgan
```
Note that this will perform a substring match on any upscalers you have installed with Auto1111. In this case, **ESRGAN_4x*** should be selected (and is also the default).

In **!MODE = PROCESS** .prompts files, you may additionally specify **!UPSCALE_MODEL = SD**. This is a special option that uses Stable Diffusion's img2img engine to upscale your images. This will take much longer than other methods and requires a lot of GPU VRAM to reach large image sizes (~12GB of VRAM is required to output 2048x2048 images), but will potentially produce higher quality results with the ability to add detail. Use !UPSCALE_SD_STRENGTH = xxx (default is 0.3) to control denoising strength with !UPSCALE_MODEL = SD.

This option works very similarly to how the highres fix in Auto1111 does. It allows you to take an image and use Stable Diffusion to create a larger version, changing the image slightly depending on the denoising strength used (the 0.3 default value should stay very close to the original in most cases).
```
!UPSCALE_MODEL = sd
!UPSCALE_SD_STRENGTH = 0.3
```
*To use !UPSCALE_MODEL = SD, you must first add MAX_OUTPUT_SIZE to your Dream Factory config.txt file (see config-default.txt for explanation).*
#### !UPSCALE_AMOUNT
The factor to upscale by. Setting !UPSCALE_AMOUNT = 2 will double the width and height of an image (resulting in quadruple the resolution). Has no effect unless !USE_UPSCALE = yes.
```
!UPSCALE_AMOUNT = 2
```
#### !UPSCALE_CODEFORMER_AMOUNT
The visibility of [Codeformer face enhancement](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#face-restoration) on the output image. Valid values are between 0-1. Setting this to 0 disables Codeformer enhancement entirely. Has no effect unless !USE_UPSCALE = yes.
```
!UPSCALE_CODEFORMER_AMOUNT = 0.50
```
#### !UPSCALE_GFPGAN_AMOUNT
The visibility of [GFPGAN face enhancement](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#face-restoration) on the output image. Valid values are between 0-1. Setting this to 0 disables GFPGAN enhancement entirely. Has no effect unless !USE_UPSCALE = yes.
```
!UPSCALE_GFPGAN_AMOUNT = 0.50
```
#### !UPSCALE_KEEP_ORG
When upscaling, keep the original (non-upscaled) image as well? Valid options are **yes** or **no** (default). If set to yes, originals will be stored in an /originals sub-directory off the main output folder. Has no effect unless !USE_UPSCALE = yes.
```
!UPSCALE_KEEP_ORG = no
```
#### !FILENAME
Allows you to specify a custom output filename. You may use the following variables; they will be filled in when the image is created:
* ```<date>```
* ```<date-year>```
* ```<date-month>```
* ```<date-day>```
* ```<height>```
* ```<input-img>```
* ```<model>```
* ```<neg_prompt>```
* ```<prompt>```
* ```<sampler>```
* ```<scale>```
* ```<seed>```
* ```<steps>```
* ```<time>```
* ```<width>```
* ```<cn-img>```
* ```<cn-model>```
* ```<upscale-model>```

The file extension (.jpg) will be added automatically.
```
!FILENAME = <date-year><date-month><date-day>-<model>-<width>x<height>-<prompt>
```
The above example might produce an output filename of **20230209-deliberate_v11-768x1280-a-photo-of-a-cute-cat.jpg**, for example.

Note that ```<input-img>``` and ```<cn-img>``` (ControlNet input image) will be the base filename only (no subdirectories or file extension).
#### !CLIP_SKIP
Sets the [CLIP skip](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#clip-skip) value. The default is 1, and most models work best with it set there. However some models may give optimal results with other values.
```
!CLIP_SKIP = 2
```
You may set this to nothing (!CLIP_SKIP = ) to clear it.
#### !SEAMLESS_TILING
Enables or disables seamless tiling mode. When enabled, output images will be suitable for tiling without visible seams/edges.
```
!SEAMLESS_TILING = on
```
Set to **off** to disable (the default).
#### !CONTROLNET_INPUT_IMAGE
Sets an input image for use with ControlNet.
```
!CONTROLNET_INPUT_IMAGE = poses\examples\openpose-standing_arms_in_front.png
```
The above example will use **openpose-standing_arms_in_front.png** as the ControlNet input image. Note that this will have no effect if you do not have the ControlNet extension installed, and/or you do not also specify a ControlNet model via the [!CONTROLNET_MODEL](https://github.com/rbbrdckybk/dream-factory/tree/main/README.md#controlnet_model) directive.

You may clear previously-set input images by issuing another directive to set it to nothing (!CONTROLNET_INPUT_IMAGE = ).

Note that you may also pass a directory of images to this directive:
```
!CONTROLNET_INPUT_IMAGE = poses\examples
```
If a directory is passed, every image in the folder will be applied to the prompt(s) that follow.
#### !CONTROLNET_MODEL
Sets the ControlNet model to use.
```
!CONTROLNET_MODEL = openpose
```
You may press control-H (or press the appropriate button) within the integrated editor to open a reference that displays your available ControlNet models. Note that setting a ControlNet model will have no effect if you do not have the ControlNet extension installed, and/or you do not also specify a ControlNet input image via the [!CONTROLNET_INPUT_IMAGE](https://github.com/rbbrdckybk/dream-factory/tree/main/README.md#controlnet_input_image) directive.

Note that you may optionally specify **auto** for !CONTROLNET_MODEL (or **auto, [default]**) if you want Dream Factory to extract the model from your [!CONTROLNET_INPUT_IMAGE](https://github.com/rbbrdckybk/dream-factory/tree/main/README.md#controlnet_input_image) filename(s). You must name your image in the following format for this to work: ```[ControlNet model to use]-[rest of filename].ext```. For example, an image named **openpose-standing_arms_in_front.png** would indicate that the openpose model should be used when !CONTROLNET_MODEL = auto.
```
!CONTROLNET_MODEL = auto, depth
```
In this example directive, Dream Factory will attempt to extract the model to use from your filenames, and fallback to 'depth' as a default model if your filename didn't contain a valid model. Specifying a default is optional, but if a model cannot be discerned from your filename(s) and no default is present, ControlNet will be disabled.

Note: this uses a substring match on the valid server values available via the integrated reference, so for example if 'control_canny-fp16' is what the reference reports, then setting **!CONTROLNET_MODEL = canny** will find it.
#### !CONTROLNET_PRE
Sets the ControlNet preprocessor to use. This is used to "extract" pose information from a normal image, so that it can then be used with the corresponding ControlNet model. If you're using pre-generated poses (such as the example ones contained in the Dream Factory **poses** folder) you do not need to set this (or you can set it to the default of 'none').
```
!CONTROLNET_PRE = openpose
```
You may press control-H (or press the appropriate button) within the integrated editor to open a reference that displays your available ControlNet preprocessors. Note that setting a ControlNet preprocessor will have no effect if you do not have the ControlNet extension installed, and/or you do not also specify a ControlNet input image via the [!CONTROLNET_INPUT_IMAGE](https://github.com/rbbrdckybk/dream-factory/tree/main/README.md#controlnet_input_image) directive.
#### !CONTROLNET_GUESSMODE
*GUESSMODE is no longer supported as of CN extension v1.1.09 - see below for the replacement!*

Use this to enable (yes) or disable (no, the default) guess mode (or "non-prompt mode") when using ControlNet. 
```
!CONTROLNET_GUESSMODE = yes
```
You can [read about guess mode here](https://github.com/lllyasviel/ControlNet#guess-mode--non-prompt-mode).
#### !CONTROLNET_CONTROLMODE
Use this to tell ControlNet to favor your prompt more than ControlNet, or vice-versa, or take a balanced approach. Options are '**balanced**' (default), '**prompt**' (to favor your prompt more), or '**controlnet**' (to favor ControlNet more). 
```
!CONTROLNET_CONTROLMODE = balanced
```
You can [read about control mode here](https://github.com/Mikubill/sd-webui-controlnet/issues/1011).
#### !CONTROLNET_PIXELPERFECT
Use this to enable (yes) or disable (no, the default) pixel perfect mode when using ControlNet. When enabling this, the image height and width you specified (with !WIDTH and !HEIGHT) will be used to generate ControlNet's preprocessed image.
```
!CONTROLNET_PIXELPERFECT = yes
```
#### !CONTROLNET_LOWVRAM
Use this to enable (yes) or disable (no, the default) low VRAM mode when using ControlNet. 
```
!CONTROLNET_LOWVRAM = yes
```
This may be helpful if you have a GPU with less VRAM.
#### !AUTO_SIZE
Allows you to have Dream Factory automatically size your output images based in the size of input images or ControlNet input images. Valid options are **match_input_image_size**, **match_controlnet_image_size**, **match_input_image_aspect_ratio**, **match_controlnet_image_aspect_ratio**, **resize_longest_dimension:[size]**, or **off** (default).
```
# output image will be set to the same size as your input image, regardless of any !WIDTH & !HEIGHT directives
!AUTO_SIZE = match_input_image_size

# output image will use the larger of your !WIDTH & !HEIGHT directives as the longer output dimension
# the shorter output dimension will be calculated so that the output image has the same aspect ratio as the ControlNet input image
!AUTO_SIZE = match_controlnet_image_aspect_ratio

# the output image will be re-sized so that the longer of your !WIDTH/!HEIGHT settings becomes the size specified here
# the shorter dimension will be calculated to maintain the same aspect ratio as the original !WIDTH/!HEIGHT settings
# useful if you have an existing prompt file full of size directives and want to quickly change the size on all of them
!AUTO_SIZE = resize_longest_dimension: 1280
```
Note that all resizings will result in image dimensions that are divisible by 64 (both dimensions will be rounded down to the nearest divisible-by-64 number).

For example, with **!AUTO_SIZE = match_controlnet_image_aspect_ratio**, if you set both your !WIDTH and !HEIGHT to 1408, and pass a 1920x1080 ControlNet input image (16:9 aspect ratio), the resulting output image will be 1408x768. The larger dimension has been set to the larger of your !WIDTH & !HEIGHT setting, and the smaller dimension has been calculated to be as close as possible to a 16:9 aspect ratio with a smaller dimension that is evenly divisble by 64.
#### IPTC_TITLE
Sets the image's title in embedded [IPTC metadata](https://www.iptc.org/standards/photo-metadata/). Generally only useful if you plan to export your images into some other application that uses IPTC standards for cataloging, etc.
```
IPTC_TITLE = Super awesome AI kitten image!
```
Set this to nothing to clear it, as usual.
#### IPTC_DESCRIPTION
Sets the image's description in embedded [IPTC metadata](https://www.iptc.org/standards/photo-metadata/). Generally only useful if you plan to export your images into some other application that uses IPTC standards for cataloging, etc.
```
IPTC_DESCRIPTION = This is an excellent AI image of a cute kitten.
```
Set this to nothing to clear it, as usual.
#### IPTC_KEYWORDS
Sets the image's keywords in embedded [IPTC metadata](https://www.iptc.org/standards/photo-metadata/). Generally only useful if you plan to export your images into some other application that uses IPTC standards for cataloging, etc. Keywords should be a comma-separated list.
```
IPTC_KEYWORDS = ai, kitten, cute
```
Set this to nothing to clear it, as usual.
#### IPTC_COPYRIGHT
Sets the image's copyright statement in embedded [IPTC metadata](https://www.iptc.org/standards/photo-metadata/). Generally only useful if you plan to export your images into some other application that uses IPTC standards for cataloging, etc.
```
IPTC_COPYRIGHT = Copyright © 2023 Super Awesome Image Studio
```
Set this to nothing to clear it, as usual.
#### !REPEAT
Tells Dream Factory whether or not to continuing producing images after it has finished all possible combinations in the prompt file. Options are **yes** (default) or **no**. If set to no, Dream Factory will idle after it has completed all prompts.
```
!REPEAT = yes
```
#### !NEXT_PROMPT_FILE
Allows you to specify another prompt file to load when the current file finishes processing. Do not include a path; Dream Factory will automatically look for prompt files in the prompt location specified in your config.txt file. Note that this will have no effect in random prompt files or standard prompt files with *!REPEAT = yes*, since those files will run forever.
```
!NEXT_PROMPT_FILE = example-random
```
A .prompts file extension will be appended automatically if you omit it.
#### !MIN_SCALE
When using random mode prompt files, sets the minimum !SCALE value to use. If !MIN_SCALE and !MAX_SCALE are set to different values, Dream Factory will choose a random value between them for each prompt.
```
!MIN_SCALE = 6.0
```
*Deprecated - consider using !SCALE = x.x - xx.x format instead.*
#### !MAX_SCALE
When using random mode prompt files, sets the maximum !SCALE value to use. If !MIN_SCALE and !MAX_SCALE are set to different values, Dream Factory will choose a random value between them for each prompt.
```
!MIN_SCALE = 18.5
```
*Deprecated - consider using !SCALE = x.x - xx.x format instead.*
#### !MIN_STRENGTH
When using random mode prompt files, sets the minimum !STRENGTH value to use. If !MIN_STRENGTH and !MAX_STRENGTH are set to different values, Dream Factory will choose a random value between them for each prompt.
```
!MIN_STRENGTH = 0.45
```
*Deprecated - consider using !STRENGTH = 0.xx - 0.xx format instead.*
#### !MAX_STRENGTH
When using random mode prompt files, sets the maximum !STRENGTH value to use. If !MIN_STRENGTH and !MAX_STRENGTH are set to different values, Dream Factory will choose a random value between them for each prompt.
```
!MAX_STRENGTH = 0.80
```
*Deprecated - consider using !STRENGTH = 0.xx - 0.xx format instead.*
#### !RANDOM_INPUT_IMAGE_DIR
When using random mode prompt files, sets a directory that random input images should be pulled from. If this is set, Dream Factory will choose a random input image to use for each prompt.
```
!RANDOM_INPUT_IMAGE_DIR = C:\images                      # specifies the full path to a directory containing input images
!RANDOM_INPUT_IMAGE_DIR = images                         # specifies a relative path to a directory containing input images
!RANDOM_INPUT_IMAGE_DIR =                                # specifies no input images should be used
```

## Viewing your Images

You can click 'Gallery' in the top nav from any page to see the images that Dream Factory has produced for you. By default, you'll be looking at the most recently-created 200 images (the max number of images to display can be changed in your config.txt file via the GALLERY_MAX_IMAGES setting). You can also select a specific output folder to browse via the dropdown near the top of the page.

When selecting a specific folder to browse, a zip icon will appear next to the folder name. Clicking this will download the entire folder of images as a .zip file.

Clicking any image will open an expanded view of that image, and also display the selected image's associated metadata. While viewing an image, there are several additional commands available - these are represented by icons located over the image. Mousing over each icon will bring up a help bubble explaining the how each works, along with the command's associated hotkey (e.g.: left and right arrow keys to browse images, 'del' to delete an image, etc.).

When deleting images via the hotkey (the 'del' key), note that the confirmation dialog is disabled to allow you to quickly delete large numbers of images (clicking the delete icon above the image will prompt you to confirm the deletion via an additional popup). If you accidentally delete images that you meant to keep, you can recover them in your ```[dream factory]/server/temp``` folder **before** you shut Dream Factory down (this folder is cleaned out on every shutdown!).

While Dream Factory is not really intended to be used on mobile devices, you can swipe left and right when viewing images in the gallery to quickly browse. Swiping down while viewing an image will bring up the delete confirmation dialog. Swipe interactions have only been tested on Chrome for Android and aren't guaranteed to work properly on other mobile platforms.

# Advanced Usage

Some usage scenarios for more advanced users can be found here.

## Wildcards

Wildcard files are simple text files placed into your dream-factory/prompts/wildcards directory. You can reference these wildcards by using `__[wildcard filename]__` (that's 2 underscores, followed by the wildcard filename without the .txt extension, followed by 2 more underscores) from within any of your prompt file [prompts] sections. When Dream Factory builds the final prompt, it'll replace the wildcard reference with a random line from the file.

You can press ctrl+h or click the help button when editing prompt files with the integrated editor to see a list of your available wildcards (click one to copy it to the clipboard for easy inclusion in your prompt files!).

An example colors.txt file is included. Specifying `__colors__` in any of your prompts will pull in a random color.

Nested wildcards (references to wildcards within a wildcard file) are permitted (as of 2023-02-16).

## Custom Models

Any custom models that you've placed in your Auto1111 models directory are available to use within Dream Factory via the [!CKPT_FILE directive](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#ckpt_file). For models that require a trigger word (for example, the [Mo-Di model](https://huggingface.co/nitrosocke/mo-di-diffusion) requires you to place the phrase 'modern disney style' somewhere in your prompt), you can have Dream Factory automatically insert these for you.

After each Dream Factory startup (after the first GPU is fully initialized), a **model-triggers.txt** file will be created/updated in your Dream Factory root folder. Each of your available models should show up in this file, followed by a comma. To associate a trigger phrase/token with a model, simply place it after the comma for that model's entry. For example, the following entry would associate 'modern disney style' with the model named 'moDi-v1-pruned.ckpt':
```
moDi-v1-pruned.ckpt [ccf3615f], modern disney style
```
You can control the placement of the auto-inserted trigger word with [!AUTO_INSERT_MODEL_TRIGGER](https://github.com/rbbrdckybk/dream-factory/blob/main/README.md#auto_insert_model_trigger).

## Embeddings

If you've installed any [textual inversion embeddings into your Auto1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Textual-Inversion) SD webui, you can reference them via the integrated prompt editor's built-in help.

Just press ctrl+h or click the help button when editing prompt files with the integrated editor to see a list of your available embeddings (click one to copy it to the clipboard for easy inclusion in your prompt files!).

## ControlNet

(2023-03-13 Note: this should be considered WIP - the editor reference pages are pretty rough and there may be some bugs!)

If you've installed the [Auto1111 ControlNet extension](https://github.com/Mikubill/sd-webui-controlnet) and have at least one of ControlNet [pre-trained models](https://civitai.com/models/9251/controlnet-pre-trained-models) installed, then ControlNet functionality should automatically be enabled within Dream Factory.

### ControlNet Prompt File Directives

You can reference current [ControlNet prompt file directives here](https://github.com/rbbrdckybk/dream-factory#controlnet_input_image).

Note that at minimum, you'll need to set both **!CONTROLNET_INPUT_IMAGE** and **!CONTROLNET_MODEL** in your prompt file to activate ControlNet.

### ControlNet Poses

If you have a library of ControlNet poses, you may place them into the **poses** directory located off your main Dream Factory folder. Pose image files may be organized into their own folders (no more than one level deep).

Optional: you may additionally create a **previews** sub-directory in each of these folders. Within the **previews** sub-folder, you may place a rendered image that corresponds to each pose file - these previews must be named the same as the pose file (though you may have different image formats; currently .jpg or .png will work). These previews will appear alongside the pose image files in the Dream Factory integrated prompt editor reference.

Check out the **poses\examples** Dream Factory folder for a couple examples of pose image files, and their corresponding preview files. You should be able to view these within the Dream Factory prompt file editor reference area (press control-H while editing any prompt file to open).

### ControlNet Tips
* If you do not want the pre-processor image map as an additional output when using the **!CONTROLNET_PRE** directive, you may disable this within the Auto1111 UI. Go to Settings -> ControlNet -> Do not append detectmap to output.

# Updating Dream Factory

You can update Dream Factory to the latest version by typing:
```
python setup.py --update
```

# Troubleshooting

Fixes for common issues may be found here.

## Compatibility with Automatic1111

Due to Automatic's lack of a clear license for his Automatic1111 repo, I've elected to not package Dream Factory with it's own version of the Automatic1111 SD webui. If Automatic makes significant changes to Automatic1111 in the future, it's possible that Dream Factory may stop working. I'll try to keep this updated with the hash to the latest known-working version of Automatic1111 in case issues arise.

You can grab a known-compatible version of Automatic1111's SD webui by going to your Auto1111 installation directory and typing this at the command-line:
```
git checkout baf6946e06249c5af9851c60171692c44ef633e0
```
If you get an error that the hash reference is not a tree, run ```git pull``` and try again.

If/when you want to go back to the latest version, you can just run ```git checkout master```.

(updated 2023-06-04, previous supported hash: 20ae71faa8ef035c31aa3a410b707d792c8203a3)
