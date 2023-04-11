# Screen Recorder

Here we have a custom screen recording tool that we use for reviewing purposes.
The goal of this tool is to allow each artist to:

quickly take descriptive turntables or flythroughs of the current work,
have the data automatically organized for easy and hassle-free playlist generation for daily reviews in the meeting room.

# Usage

When launching the tool from the latest build .exe or from THNScreenRecorderMain.py, the screen recording frame pops up (green frame border).

Place the frame properly to best showcase your contents (no specific aspect ratio is required, it will be conformed automatically).

You can click-drag the frame around, and expand/contract it by dragging the corners.

![01](https://user-images.githubusercontent.com/19984246/231102484-6dd4e9ca-0bfd-4818-84ea-189d4979a191.jpg)


Type in the text bar at the top the name of the capture with the asset you're showcasing for review. It should be one or two words, just the item name (or the location, in case of a flythrough).

From the drop down menu, pick the project that the asset belongs to.

![02](https://user-images.githubusercontent.com/19984246/231102586-c4d52b45-39a0-4a98-b1e6-f9bac1c0c5e1.jpg)

Hit the Record button to start recording your screen.

The border will change to red and the record button will change to a timer so you can see how long the recording has been, try not to have too many heavy apps (aka 3d editors) open at the same time while recording.

Orbit around the asset, rotate it, showcase UVs, details, swing the light around, or fly around the location if it's a flythrough.

The screen recorder will also take in to account the time of day and anything recorded after 10.30am will go in the folder for the next day and if it's before, it will go in the current day's folder. This will help keep captures organised and date on the slate at the beginning of the recordings should be the same as the day the asset will be reviewed. 

Important: keep it short and descriptive, to the point. Try to stay under 60 secs, but feel free to create multiple takes, this is where the Pause button will be very useful. If the recording is paused the frame can be moved or resized and another area in the level can be navigated to before resuming, this will create a clip with less unnecessary flying around. It will also speed up the frame processing stage as few frames will be captured.


![04](https://user-images.githubusercontent.com/19984246/231102778-5abe7380-bb26-4c32-8ee8-73ae3c64b66d.png)


Hit the Stop Record to end the recording and start the frame processing.

You're done. You can proceed to the meeting room when the daily review meeting is due and your capture will be part of the reviewed playlist.

Note: as you hit Stop Record to end the capture, a series of processes will start in under the hood, you can see how long the processing is taking via a progress bar in the main UI.

If you close the app while the frames are being created the process will stop and you will only have a partial sequence of images. This can be useful if you create a long recording and decide that you don't want to keep it. The frames will still be in the review folder however and should be deleted manually or overwritten.

![05](https://user-images.githubusercontent.com/19984246/231102981-b7be599e-de29-415d-ba83-b59d477c8d0a.png)


