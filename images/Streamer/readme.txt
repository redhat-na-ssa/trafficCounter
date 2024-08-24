# Command to capture video from stream
ffmpeg -i https://sfs-lr-36.dot.ga.gov:443/rtplive/GDOT-CCTV-0135/playlist.m3u8 -t 00:02:00 -c copy output.mp4


# Command to convert mp4 to streaming format
ffmpeg -i videos/gdot-camera01.mp4 -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls videos/gdot-camera01.m3u8
